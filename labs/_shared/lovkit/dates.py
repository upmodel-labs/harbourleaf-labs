from datetime import date

# A fixed date, so a rule such as "not before the reference date" gives the same
# answer on every day it is run. Never compare against today's date in these labs.
REFERENCE_DATE = date(2026, 11, 12)
