import csv
import json
import os
import sys
import configparser
from datetime import datetime
import requests
from dateutil import tz

cfg = configparser.ConfigParser()
cfg.read('settings.conf')

from_zone = tz.gettz(cfg['time']['src_timezone'])
to_zone = tz.gettz(cfg['time']['dst_timezone'])

if len(sys.argv) != 2:
    print("Usage: python script.py <transactions_file>")
    sys.exit(1)
transactions_file = sys.argv[1]


def convert_gmt_to_local(date):
    gmt_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    gmt_date = gmt_date.replace(tzinfo=from_zone)
    local_date = gmt_date.astimezone(to_zone)
    return local_date.isoformat()

def convert_eur_usd(amount, date):
    if amount != "":
        short_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
        r = requests.get('https://api.frankfurter.app/'+ short_date +'?to=USD', timeout=20)
        return float(amount)*r.json()['rates']['USD']
    return 0

with open(transactions_file, "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = { 'activities': [] }
    next(csv_file)
    for row in csv_reader:
        line = {
            "accountId": cfg['ghostfolio']['account_id'],
            "currency": cfg['ghostfolio']['currency'],
            "dataSource": cfg['ghostfolio']['data_source'],
            "date": convert_gmt_to_local(row[1]),
            "fee": convert_eur_usd(row[7], row[1]),
            "quantity": float(row[3]),
            "symbol": cfg['ghostfolio']['symbol'],
            "type": "BUY", #We don't sell, HODL
            "unitPrice": float(convert_eur_usd(row[11], row[1]))
        }
        data['activities'].append(line)

# Write output to json file with the same name as input file
output_file = f"{os.path.splitext(transactions_file)[0]}.json"
with open(output_file, 'w') as json_file:
    json.dump(data, json_file, indent=2)

print(f"Data written to {output_file}")