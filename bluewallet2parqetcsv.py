#!/usr/bin/env python3
'''
Stefan Lohmaier <stefan@slohmaier.de>, hereby disclaims all copyright interest in the program “mintoscsv2parqetcsv” (which deconstructs trees) written by James Hacker.
---
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
'''
import argparse
import csv
import os
import pandas as pd
import requests
import sys
import time
from datetime import datetime, timedelta

pd.set_option('expand_frame_repr', False)

_MONTHDICT = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}

def get_price(d: datetime) -> float:
    #construct url with timestamp in unix time fromat
    url = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym=BTC&tsyms=EUR&ts='
    url += str(int(time.mktime(d.timetuple())))

    response = requests.get(url)
    return float(response.json()['BTC']['EUR'])

if __name__ == '__main__':
    argparser = argparse.ArgumentParser('bluewallet2parqetcsv',
        description='Convert Bluewallet CSV\'s to Parqet CSV\'s.')
    argparser.add_argument('--bcsv', '-b', dest='bcsv', required=True,
        help='path to BlueWallet CSV')
    argparser.add_argument('--pcsv', '-p', dest='pcsv', required=True,
        help='output path for Parqet Cash CSV')

    args = argparser.parse_args()
    #fod code completion
    args.bcsv = args.bcsv
    args.pcsv = args.pcsv
    
    if not os.path.isfile(args.bcsv):
        sys.stderr.write('Blue Wallet CSV "{0}" is not a file! Try {1} -h.\n'
            .format(args.ecsv, sys.argv[0]))
        sys.exit(1)
    
    bcsvFile = open(args.bcsv, 'r')
    bcsv = csv.reader(bcsvFile, delimiter=',')

    rows = []
    for row in bcsv:
        date = row[0]
        if date == 'Datum':
            continue
        for month in _MONTHDICT.keys():
            date = date.replace(' '+month+' ', ' '+_MONTHDICT[month]+' ')
        date = date.split(' ')
        timeStr = date[4]
        timeParts = timeStr.split(':')
        dateStr = '{0}-{1}-{2}'.format(date[3], date[1], date[2])
        dt = datetime(
            int(date[3]),
            int(date[1]),
            int(date[2]),
            int(timeParts[0]),
            int(timeParts[1]),
            int(timeParts[2])
        )

        _type = 'TransferIn'
        assetType = 'Crypto'
        identifier = 'BTC'
        shares = row[2]
        price = str(int(get_price(dt)))
        currency = 'EUR'
        tax = '9'
        fee = '0'

        rows.append([dateStr, timeStr, identifier, shares, assetType, _type, price, currency, tax, fee])

    pcsvFile = open(args.pcsv, 'w+')
    pcsv = csv.writer(pcsvFile, 'unix', quoting=0, delimiter=';')
    pcsv.writerow(['date', 'time', 'identifier', 'shares', 'assetType', 'type', 'price', 'currency', 'tax', 'fee'])

    for row in rows:
        pcsv.writerow(row)

    bcsvFile.close()
    pcsvFile.close()
