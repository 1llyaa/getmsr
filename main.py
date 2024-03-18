import requests
import time
import toml
import csv
from getpass import getpass
from requests.auth import HTTPBasicAuth
from tinydb import TinyDB, Query


db = TinyDB("msr.json")
Todo = Query()


def create_config():
    with open("config.toml", "w") as f:
        f.write("[config]\n")
        f.write(f"server = " + "'" + input("Server adress: ") + "'" + "\n")
        f.write(f"count_of_attempts = " + input("Count of attempts: ") + "\n")
        f.write(f"time_to_wait = " + input("Time to wait between record: ") + "\n")


def load_config(config_name="config.toml"):
    with open(config_name, "r") as f:
        data = toml.load(f)
        ip = data['config']['server']
        count_of_attempts = data['config']['count_of_attempts']
        time_to_wait = data['config']['time_to_wait']
    return ip, count_of_attempts, time_to_wait


def main():
    # load config
    ip = load_config()[0]
    username = getpass(prompt='Username: ', stream=None)
    password = getpass(prompt='Password: ', stream=None)
    count_of_attempts = load_config()[1]
    time_to_wait = load_config()[2]

    # delete last database
    db.truncate()

    for i in range(count_of_attempts):
        time.sleep(time_to_wait)

        response = requests.get(ip, verify=False, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            db.insert(response.json())
            print(f"Záznam proběhl úspěšně: {response.json}")

        elif response.status_code == 401:
            print(f"Unauthorized access (mostly cause wrong password or user): {response.status_code}")
            break

        else:
            print(f"Response code invalid: {response.status_code}")


def to_csv():
    with open('above_1500.csv', 'w') as csv_file:
        # using csv.writer method from CSV package
        write = csv.writer(csv_file)
        fields = ['CO2', 'Station', 'temperature', 'time']
        write.writerow(fields)

        list_1500 = db.search(Todo["CO2"] > 1500)

        for row in list_1500:
            write.writerow(row.values())


if __name__ == "__main__":
    # create_config()
    main()
    to_csv()
