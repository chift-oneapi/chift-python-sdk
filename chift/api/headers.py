import contextlib
import datetime
from collections.abc import Mapping
from contextvars import ContextVar
from dataclasses import dataclass
from functools import cached_property
from typing import Callable, Generator, Literal, Optional, Protocol, TypeVar, cast

from requests.structures import CaseInsensitiveDict

T = TypeVar("T")

DatalayerSource = Literal["datalayer", "classic"]


@dataclass(frozen=True)
class DatalayerHeaders:
    source: DatalayerSource
    synced_at: Optional[datetime.datetime] = None
    covered_from: Optional[datetime.date] = None


@dataclass(frozen=True)
class CombinedDatalayerHeaders:
    # "mixed" when the responses disagree: the backend picks the source per request, so an
    # `if_available` pagination can fall back to the live connector part way through.
    source: Literal["datalayer", "classic", "mixed"]
    synced_at: Optional[datetime.datetime] = None
    covered_from: Optional[datetime.date] = None


class Response(Protocol):
    """What is read off a `requests.Response`, or the `httpx.Response` of a test client."""

    headers: Mapping[str, str]
    status_code: int


class ResponseHeaders(Mapping):
    """The headers of one response, looked up case-insensitively."""

    def __init__(
        self, headers: Mapping[str, str], method: str, path: str, status_code: int
    ):
        self._headers = CaseInsensitiveDict(headers)
        self.method = method
        self.path = path
        self.status_code = status_code

    def __getitem__(self, key: str) -> str:
        return self._headers[key]

    def __iter__(self):
        return iter(self._headers)

    def __len__(self) -> int:
        return len(self._headers)

    def __repr__(self) -> str:
        return f"<ResponseHeaders {self.method} {self.path} {self.status_code}>"

    @cached_property
    def datalayer(self) -> Optional[DatalayerHeaders]:
        """None when the request did not ask for the datalayer."""
        source = self.get("x-chift-datalayer-source")
        if not source:
            return None
        return DatalayerHeaders(
            source=cast(DatalayerSource, source),
            synced_at=_parse(
                self.get("x-chift-datalayer-synced-at"),
                datetime.datetime.fromisoformat,
            ),
            covered_from=_parse(
                self.get("x-chift-datalayer-covered-from"),
                datetime.date.fromisoformat,
            ),
        )


class CapturedHeaders(list):
    """One `ResponseHeaders` per request, in the order they were sent."""

    @property
    def last(self) -> Optional[ResponseHeaders]:
        return self[-1] if self else None

    @property
    def datalayer(self) -> Optional[CombinedDatalayerHeaders]:
        """Freshness across every captured response, taking the worst case of each field so
        that it holds for all the data read: the oldest sync and the latest start of coverage.
        """
        seen = [headers.datalayer for headers in self if headers.datalayer is not None]
        if not seen:
            return None
        sources = {freshness.source for freshness in seen}
        synced = [freshness.synced_at for freshness in seen if freshness.synced_at]
        covered = [
            freshness.covered_from for freshness in seen if freshness.covered_from
        ]
        return CombinedDatalayerHeaders(
            source=sources.pop() if len(sources) == 1 else "mixed",
            synced_at=min(synced) if synced else None,
            covered_from=max(covered) if covered else None,
        )


_collectors: ContextVar[tuple] = ContextVar("chift_captured_headers", default=())


@contextlib.contextmanager
def capture_headers() -> Generator[CapturedHeaders, None, None]:
    """Collect the response headers of every request sent inside the block.

    Requests are sent when the SDK call runs, so a generator such as `iter_all` must be
    consumed inside the block for its pages to be captured.
    """
    captured = CapturedHeaders()
    token = _collectors.set(_collectors.get() + (captured,))
    try:
        yield captured
    finally:
        _collectors.reset(token)


def record_response(response: Response, method: str, path: str) -> None:
    collectors = _collectors.get()
    if not collectors:
        return
    headers = ResponseHeaders(response.headers, method, path, response.status_code)
    for captured in collectors:
        captured.append(headers)


def _parse(value: Optional[str], parser: Callable[[str], T]) -> Optional[T]:
    if not value:
        return None
    try:
        return parser(value)
    except ValueError:
        return None
