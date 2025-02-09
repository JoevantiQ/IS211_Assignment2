import argparse
import urllib.request
import logging
import csv
from datetime import datetime

URL = "https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv"


def downloadData(url):
    """Download the data from the given URL and return it as a decoded string."""
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def processData(file_content):
    """Process the file content and return a dictionary mapping IDs to (name, birthday)."""
    data_dict = {}
    logger = logging.getLogger('assignment2')

    lines = file_content.strip().split('\n')
    reader = csv.reader(lines)
    next(reader)  # Skip header

    for line_num, row in enumerate(reader, start=1):
        try:
            id, name, birthday_str = row
            birthday = datetime.strptime(birthday_str, '%d/%m/%Y').date()
            data_dict[int(id)] = (name, birthday)
        except (ValueError, IndexError):
            logger.error(f"Error processing line #{line_num} for ID #{row[0]}")

    return data_dict


def displayPerson(id, personData):
    """Display a person's information given their ID."""
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday}")
    else:
        print("No user found with that ID")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default=URL, help='URL of the CSV file')
    args = parser.parse_args()

    logging.basicConfig(filename='errors.log', level=logging.ERROR)

    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    personData = processData(csvData)

    while True:
        try:
            user_input = int(input("Enter an ID to lookup (0 or negative to exit): "))
            if user_input <= 0:
                break
            displayPerson(user_input, personData)
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
