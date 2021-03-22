#!/usr/bin/env python3

from pymarc import MARCReader

if __name__ == '__main__':
    with open('data/bibs-obiekt_trojwymiarowy.marc', 'rb') as fh:
        reader = MARCReader(fh)
        for record in reader:
            print(record)
