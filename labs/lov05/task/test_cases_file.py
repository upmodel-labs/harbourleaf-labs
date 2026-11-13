"""Step 3: your case file must be well formed. The checks are supplied; the cases are yours to write in cases.json."""
from cases_io import load_cases, problems


def test_the_case_file_is_well_formed():
    assert problems(load_cases()) == []
