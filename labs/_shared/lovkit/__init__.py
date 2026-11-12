"""lovkit: the small shared kit for the LLM and agent output validation labs.

Standard library plus pydantic only. No live model is called: the fake
assistants below are deterministic, and their defects are switched on by flags.
Practice data only.
"""
from .dates import REFERENCE_DATE
from .members import MEMBERS
from .fake_notes import fake_notes_model
from .fake_booking import FakeBookingAssistant, make_requests
from .fake_grounded import FakeGroundedAssistant, load_corpus, line_ids, manifest_of, checksum

__all__ = ["REFERENCE_DATE", "MEMBERS", "fake_notes_model", "FakeBookingAssistant", "make_requests",
           "FakeGroundedAssistant", "load_corpus", "line_ids", "manifest_of", "checksum"]
