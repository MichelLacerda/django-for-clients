def directory_path(instance, filename):
    """."""
    from datetime import datetime
    dt = datetime.today()
    return 'user/{year}/{month}/{file}'\
        .format(year=dt.year, month=dt.month, file=filename)
