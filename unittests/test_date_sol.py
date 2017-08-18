import datetime

import pytest

from lib.date_sol import convert_timedelta_to_sol, add_sol_to_date


@pytest.mark.unittest
def test_convert_timedelta_to_sol():
    assert convert_timedelta_to_sol(datetime.date(2007, 12, 5), datetime.date(2007, 12, 6)) == 0
    assert convert_timedelta_to_sol(datetime.date(2007, 12, 5), datetime.date(2007, 12, 7)) == 1


@pytest.mark.unittest
def test_add_sol_to_date():
    assert add_sol_to_date(datetime.datetime(2007, 12, 5), 0) == datetime.datetime(2007, 12, 5)
    assert ((add_sol_to_date(datetime.datetime(2007, 12, 5), 1) - datetime.datetime(2007, 12, 5)).
            total_seconds()) == 88775.244147
