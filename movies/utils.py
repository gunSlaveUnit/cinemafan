"""Contains auxiliary set of functions for the package."""

def form_periods_movie_showing(years: list[int]) -> str:
    """
    Makes a template-ready string - what time movie was shown.

    If there are several years in ascending order,
    write the first and last, with a dash between them.
    If not, a comma.

    Args:
        years (list[int]): List of years to format.

    Returns:
        str: Formatted string of years,
            ready to be inserted into a template
            as the period in which the movie was shown.
    """

    years = sorted(set(years))
    
    periods = []
    period_start = years[0]
    previous = years[0]
    
    for year in years[1:] + [None]:
        if year != previous + 1:
            if period_start != previous:
                periods.append(f"{period_start} - {previous}")
            else:
                periods.append(str(period_start))
            period_start = year
        previous = year
    
    return ", ".join(periods)
