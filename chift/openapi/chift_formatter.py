import re

from datamodel_code_generator.format import CustomCodeFormatter


class CodeFormatter(CustomCodeFormatter):
    def apply(self, code: str) -> str:
        code = re.sub(r"^from\s+datetime\s+import\s+.*$\n?", "", code, flags=re.M)
        code = re.sub(
            r"(:\s*(?:Optional\[\s*)?)datetime(?=\s*(?:\]\s*)?(?:=|$))",
            r"\1DateTime",
            code,
            flags=re.M,
        )
        code = re.sub(
            r"(:\s*(?:Optional\[\s*)?)date(?=\s*(?:\]\s*)?(?:=|$))",
            r"\1Date",
            code,
            flags=re.M,
        )
        alias = "from datetime import date as Date, datetime as DateTime"
        if alias not in code:
            code = alias + "\n\n" + code.lstrip()
        return code
