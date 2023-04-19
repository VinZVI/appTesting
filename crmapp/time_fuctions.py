from datetime import datetime, timedelta, time


def round_dt_to_delta(dt: datetime = datetime.now(), delta: timedelta = timedelta(minutes=30)) -> time:
    """Округляет время до периода бронирования столов
    :param dt: Timestamp to round (default: now)
    :param delta: Lapse to round in minutes (default: minutes=30)
    """
    ref = datetime.min.replace(tzinfo=dt.tzinfo)
    return ref + round((dt - ref) / delta) * delta
