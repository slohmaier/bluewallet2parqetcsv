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
import re
import sys

_MONTHDICT = {
    'Jan': '1',
    'Feb': '2',
    'Mar': '3',
    'Apr': '4',
    'May': '5',
    'Jun': '6',
    'Jul': '7',
    'Aug': '8',
    'Sep': '9',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12',
}

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
        time = date[4]
        date = '{0}-{1}-{2}'.format(date[3], date[1], date[2])

        _type = 'TransferIn'
        assetType = 'Crypto'
        identifier = 'BTC'
        amount = row[2]

        rows.append([date, time, identifier, amount, assetType, _type])

    pcsvFile = open(args.pcsv, 'w+')
    pcsv = csv.writer(pcsvFile, 'unix', quoting=0, delimiter=';')
    pcsv.writerow(['date', 'time', 'identifier', 'amount', 'assetType', 'type'])

    for row in rows:
        pcsv.writerow(row)

    bcsvFile.close()
    pcsvFile.close()
