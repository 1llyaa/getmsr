import requests
import time
import toml
from requests.auth import HTTPBasicAuth
from tinydb import TinyDB, Query




pocet_pokusu = 10
cas_cekani = 1
url = "https://192.168.9.236:5002/msr"
password = "greenfish2"
username = "student"


db = TinyDB("msr.json")


def main():
    with open('config.toml', 'r') as config_file:
        new_toml_string = toml.dump(parsed_toml, config_file)
        print(new_toml_string)
        db.truncate()

        for i in range(pocet_pokusu):
            time.sleep(cas_cekani)

            response = requests.get(url, verify=False, auth=HTTPBasicAuth(username, password))

            if response.status_code == 200:
                db.insert(response.json())
                print(f"Záznam proběhl úspěšně: {response.json}")

            else:
                print(f"Response code invalid: {response.status_code}")



def to_csv():
    pass


if __name__ == "__main__":
    main()
