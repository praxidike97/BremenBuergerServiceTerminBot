import requests
import re
import datetime
import argparse

import telegram_send


def get_next_date():
    # Get the content of the website
    response = requests.get('https://www.service.bremen.de/dienstleistungen/reisepass-beantragen-8364')
    raw_text = response.text.split("\n")
    pattern = re.compile("^([A-Z][0-9]+)+$")
    desired_line = ""

    # Search for the line with the next earliest date
    for line in raw_text:
        if re.match(r".*BürgerServiceCenter-Mitte.*Frühestmöglicher Termin.*", line):
            desired_line = line
            break

    # Get the date from the string
    raw_date = desired_line.split("</a>")[3].strip().split(" ")
    string_date = raw_date[1]
    match = re.search("[0-9][0-9]:[0-9][0-9]", raw_date[3])
    string_time = match.group(0)

    # Convert to datetime object
    next_date = datetime.datetime.strptime(string_date + "  " + string_time, "%d.%m.%y %H:%M")

    return next_date


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finds the next date to get a Reisepass at the Bürgeramt Bremen')
    parser.add_argument('-b', '--before', type=str, help='Check if there is a appointment before this date')

    args = parser.parse_args()

    threshold_date = datetime.datetime.strptime(args.before, "%d.%m.%y %H:%M")
    next_date = get_next_date()

    if next_date < threshold_date:
        telegram_send.send(messages=[f'Es ist ein früherer Termin verfügbar! Datum: {next_date.strftime("%d.%m.%y %H:%M")}'])