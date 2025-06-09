import http.client as httplib
import json
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from chift.api import exceptions


class ChiftAuth(requests.auth.AuthBase):
    def __init__(
        self, client_id, client_secret, account_id, url_base, env_id, test_client
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.account_id = account_id
        self.url_base = url_base
        self.env_id = env_id
        self.test_client = test_client
        self.request_engine = self.test_client or requests

        self.access_token = None
        self.expires_at = None

    def __call__(self, request):
        request.headers.update(self.get_auth_header())
        return request

    def get_auth_header(self):
        return {"Authorization": f"Bearer {self.get_access_token()}"}

    def _parse_token(self, token):
        self.access_token = token.get("access_token")
        self.expires_at = datetime.fromtimestamp(token.get("expires_on"))

    def get_access_token(self):
        if self.access_token:
            if datetime.now() < self.expires_at:
                return self.access_token

        payload = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "accountId": self.account_id,
        }
        if self.env_id:
            payload["envId"] = self.env_id

        response = self.request_engine.post(self.url_base + "/token", json=payload)

        if not response.status_code == httplib.OK:
            raise exceptions.ChiftException(
                f"Error while authenticating '{response.status_code}': {response.text}"
            )

        self._parse_token(response.json())

        return self.access_token


class ChiftClient:
    session = None
    access_token = None
    auth = None
    consumer_id = None
    connection_id = None
    raw_data = None
    client_request_id = None
    related_chain_execution_id = None
    sync_id = None

    __instance = None
    __use_global = False

    def __new__(cls, **kwargs):
        """
        __use_global=True for singleton usage
        """
        if ChiftClient.__use_global:
            if ChiftClient.__instance is None:
                ChiftClient.__instance = object.__new__(cls)
            instance = ChiftClient.__instance
        else:
            instance = object.__new__(cls)

        return instance

    def __init__(self, consumer_id=None, **kwargs):
        from chift import (
            account_id,
            client_id,
            client_secret,
            related_chain_execution_id,
            sync_id,
            url_base,
        )

        self.consumer_id = consumer_id
        self.client_id = kwargs.get("client_id") or client_id
        self.client_secret = kwargs.get("client_secret") or client_secret
        self.account_id = kwargs.get("account_id") or account_id
        self.url_base = kwargs.get("url_base") or url_base
        self.env_id = kwargs.get("env_id")
        self.test_client = kwargs.get("test_client")
        self.related_chain_execution_id = (
            kwargs.get("related_chain_execution_id") or related_chain_execution_id
        )
        self.sync_id = kwargs.get("sync_id") or sync_id
        self.max_retries = kwargs.get("max_retries")
        self._start_session()

    def _start_session(self):
        self.ignored_error_codes = []
        if self.test_client:
            self.url_base = ""  # set to empty string to avoid url_base in the request
            self.test_auth = ChiftAuth(
                self.client_id,
                self.client_secret,
                self.account_id,
                self.url_base,
                self.env_id,
                self.test_client,
            )
        elif not self.session:
            self.session = requests.Session()
            self.session.auth = ChiftAuth(
                self.client_id,
                self.client_secret,
                self.account_id,
                self.url_base,
                self.env_id,
                None,
            )

            if self.max_retries:
                retries = Retry(
                    total=int(self.max_retries),
                    backoff_factor=0.1,
                    status_forcelist=[502],
                )
                self.session.mount("http://", HTTPAdapter(max_retries=retries))
                self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def make_request(
        self, request_type, url, data=None, content_type="application/json", params=None
    ):
        if not params:
            params = {}

        if isinstance(data, str):
            data = json.loads(data)

        headers = {
            "Content-Type": content_type,
            "Accept": "application/json",
            "User-Agent": "chift-python-sdk library",
        }

        if self.connection_id:
            headers["x-chift-connectionid"] = self.connection_id

        if self.raw_data:
            headers["x-chift-raw-data"] = "true"

        if self.client_request_id:
            headers["x-chift-client-requestid"] = self.client_request_id

        if self.related_chain_execution_id:
            headers["x-chift-relatedchainexecutionid"] = self.related_chain_execution_id

        if self.sync_id:
            headers["x-chift-syncid"] = self.sync_id

        if self.ignored_error_codes:
            headers["x-chift-ignored-error-codes"] = ",".join(self.ignored_error_codes)

        try:
            req = self.process_request(
                request_type, url, headers=headers, params=params, json=data
            )
        except requests.exceptions.RetryError as e:
            raise exceptions.ChiftException(
                f"After {self.max_retries} retries, the request failed."
            )

        if req.status_code == httplib.UNAUTHORIZED:
            raise exceptions.ChiftException(
                "Application authentication failed",
                error_code=req.status_code,
                detail=req.text,
            )

        if req.status_code == 204:
            return True

        try:
            result = req.json()
        except:
            raise exceptions.ChiftException(f"Error parsing json response: {req.text}")

        if isinstance(result, dict) and result.get("status") == "error":
            raise exceptions.ChiftException(
                result.get("message"),
                error_code=result.get("error_code"),
                detail=result.get("detail"),
            )
        elif req.status_code not in [httplib.OK, httplib.CREATED]:
            raise exceptions.ChiftException(
                f"Error returned with status code '{req.status_code}': {req.text}"
            )
        else:
            return result

    def process_request(
        self, request_type, url_path, headers=None, params=None, json=None
    ):
        engine = self.test_client or self.session
        if self.test_client:
            headers.update(self.test_auth.get_auth_header())
        return engine.request(
            request_type,
            self.url_base + url_path,
            headers=headers,
            params=params,
            json=json,
        )

    def get(self, *args, **kwargs):
        return self.make_request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.make_request("POST", *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.make_request("PATCH", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.make_request("DELETE", *args, **kwargs)

    def path_builder(self, ordered_paths):
        if ordered_paths:
            return "/" + "/".join(
                [str(path).strip("/") for path in ordered_paths if path]
            )

    def delete_one(
        self, chift_vertical, chift_model, chift_id, params=None, extra_path=None
    ):
        url_path = self.path_builder(
            [
                "consumers" if self.consumer_id else None,
                self.consumer_id,
                chift_vertical,
                chift_model,
                chift_id,
                extra_path,
            ]
        )

        return self.delete(url_path, params=params)

    def get_one(
        self, chift_vertical, chift_model, chift_id, params=None, extra_path=None
    ):
        url_path = self.path_builder(
            [
                "consumers" if self.consumer_id else None,
                self.consumer_id,
                chift_vertical,
                chift_model,
                chift_id,
                extra_path,
            ]
        )

        return self.get(url_path, params=params)

    def get_all(self, chift_vertical, chift_model, params=None, extra_path=None):
        url_path = self.path_builder(
            [
                "consumers" if self.consumer_id else None,
                self.consumer_id,
                chift_vertical,
                chift_model,
                extra_path,
            ]
        )

        return self.get(url_path, params=params)

    def post_one(self, chift_vertical, chift_model, data, extra_path=None, params=None):
        url_path = self.path_builder(
            [
                "consumers" if self.consumer_id else None,
                self.consumer_id,
                chift_vertical,
                chift_model,
                extra_path,
            ]
        )

        return self.post(url_path, data=data, params=params)

    def update_one(
        self, chift_vertical, chift_model, chift_id, data, extra_path=None, params=None
    ):
        url_path = self.path_builder(
            [
                "consumers" if self.consumer_id else None,
                self.consumer_id,
                chift_vertical,
                chift_model,
                chift_id,
                extra_path,
            ]
        )

        return self.patch(url_path, data=data, params=params)

    def set_ignored_error_codes(self, ignored_error_codes=[]):
        self.ignored_error_codes = ignored_error_codes
