"""The result every guard returns: a decision, a reason for the log, and (for BLOCK or ESCALATE) the message the member sees."""
from typing import Literal, Optional

from pydantic import BaseModel

Decision = Literal["ALLOW", "BLOCK", "ESCALATE"]


class GuardResult(BaseModel):
    decision: Decision
    reason: str
    message: Optional[str] = None
