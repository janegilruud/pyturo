"""
    Module providing a function reading tur-O posts from CSV file.
"""
#! /usr/bin/env python3
# coding=utf-8

import sys
import argparse
import csv
from collections import namedtuple

DATA_FIELDS = ['tur', 'navn', 'kode', 'poeng', 'qr', 'beskrivelse']
Post = namedtuple('Post', DATA_FIELDS)

def main():
    """Main function"""
    args = parse_args()
    data = read_poster(args.csv)
    for post in data:
        print(post)

def parse_args():
    """Parse arguments"""
    parser = argparse.ArgumentParser(description='Read-write data')
    parser.add_argument('-csv', default='csv', help='CSV file containing information about posts')
    return parser.parse_args()

def read_poster(file_path):
    """Read poster from file and return as array"""
    poster = []
    with open(file_path, 'r', encoding="utf-8") as csvfile:
        postreader = csv.DictReader(csvfile, delimiter=',')
        for row in postreader:
            d_tur = row['Tur']
            d_navn = row['Navn']
            d_kode = row['Kode']
            d_poeng = row['Poeng']
            d_qr = row['QR']
            d_beskrivelse = row['Beskrivelse']
            poster.append(Post(d_tur, d_navn, d_kode, d_poeng, d_qr, d_beskrivelse))
        print("Size: " + str(len(poster)))
    return poster

if __name__ == "__main__":
    sys.exit(main())
