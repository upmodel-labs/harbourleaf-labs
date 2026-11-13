"""The output guard: checks the assistant's summary before it is posted. Looks for a phone number or an email address.

    check_output(reply) -> GuardResult
"""
import re

from guard_types import GuardResult

PHONE = re.compile(r"\+?\d[\d\s\-]{9,}\d")
EMAIL = re.compile(r"[\w.\-]+@[\w\-]+\.[a-z]{2,}")


def check_output(reply):
    if PHONE.search(reply):
        return GuardResult(decision="BLOCK", reason="phone number pattern",
                           message="This summary has contact details in it, so it was not posted.")
    if EMAIL.search(reply):
        return GuardResult(decision="BLOCK", reason="email pattern",
                           message="This summary has contact details in it, so it was not posted.")
    return GuardResult(decision="ALLOW", reason="no contact details found")
