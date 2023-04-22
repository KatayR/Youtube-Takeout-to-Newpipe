import datetime


def convert_date_string(date_string):
    months = {"Oca": 1, "Şub": 2, "Mar": 3, "Nis": 4, "May": 5, "Haz": 6,
              "Tem": 7, "Ağu": 8, "Eyl": 9, "Eki": 10, "Kas": 11, "Ara": 12}
# Modify the line above for the language of your html's language
    day, month_abbr, year, time_string, *_ = date_string.split()
    month_num = months[month_abbr]
    time_without_timezone = datetime.datetime.strptime(
        f"{day} {month_num} {year} {time_string}", "%d %m %Y %H:%M:%S")
    return int(time_without_timezone.timestamp())
