import datetime


months = ("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")


async def stylize_date(date_isoformat: datetime.date.isoformat) -> str:

    if (datetime.date.today() == datetime.date.fromisoformat(date_isoformat)):
        return "Сегодня"
    elif (datetime.date.today() + datetime.timedelta(days=1) == datetime.date.fromisoformat(date_isoformat)):
        return "Завтра"
    else:
        return "%s, %s" % (months[int(date_isoformat[5:6+1])-1], date_isoformat[8:9+1])


async def stylize_time(time_isoformat: datetime.time.isoformat) -> str:

    return time_isoformat[:5]