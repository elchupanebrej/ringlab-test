from datetime import timedelta
from math import ceil

sol_day_conversion_factor = 1.02749125170


def convert_timedelta_to_sol(initial_date, final_date):
    return ceil((final_date-initial_date).total_seconds()/(60*60*24*sol_day_conversion_factor)) - 1


def add_sol_to_date(initial_date, sol):
    return initial_date + timedelta(days=sol * sol_day_conversion_factor)
