from datetime import datetime as DT, time, date, timedelta


def round_dt_to_delta(dt: DT = DT.now(), delta: timedelta = timedelta(minutes=30)) -> time:
    """Округляет время до периода бронирования столов
    :param dt: Timestamp to round (default: now)
    :param delta: Lapse to round in minutes (default: minutes=30)
    """
    ref = DT.min.replace(tzinfo=dt.tzinfo)
    return ref + round((dt - ref) / delta) * delta


def get_time_period(period: time.minute) -> str:
    return (DT.combine(date.today(), time(0, 0)) + timedelta(minutes=period)).time().strftime("%H:%M")
