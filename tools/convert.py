#!/usr/bin/env python3
"""
Base code for this script was taken from https://github.com/DavidChouinard/mrc_to_csv
Code was modified to make it work with python3
"""
import csv
import os
import sys
from importlib import reload

from pymarc import MARCReader

reload(sys)
sys.setdefaultencoding('utf8')


def main():
    for filename in os.listdir('../data/mrc/'):
        if os.path.isdir('data/mrc/' + filename) or filename[0] == '.':
            continue

        with open('../data/csv/' + os.path.splitext(filename)[0] + '.csv', 'wb') as f, \
             open('../data/mrc/' + filename, 'rb') as fh:

            reader = MARCReader(fh)
            writer = csv.writer(f)
            # TODO Choose columns to convert either to csv or some other format
            writer.writerow(['isbn', 'title', 'author',
                             'publisher', 'pub_place', 'pub_year',
                             'extent', 'dimensions', 'subject', 'inclusion_date',
                             'source', 'library', 'notes'])

            for i, record in enumerate(reader):
                # print record
                pub_place = clean(record['260']['a']) if '260' in record else None
                extent = clean(record['300']['a'], True) if '300' in record else None
                dimensions = record['300']['c'] if '300' in record else None
                subject = record['650']['a'] if '650' in record else None
                inclusion_date = record['988']['a'] if '988' in record else None
                source = record['906']['a'] if '906' in record else None
                library = record['690']['5'] if '690' in record else None

                notes = " ".join([field['a'] for field in record.notes() if 'a' in field])

                writer.writerow([record.isbn(), get_title(record), clean(record.author(), True),
                                 clean(record.publisher()), pub_place, clean(record.pub_year()),
                                 extent, dimensions, subject, inclusion_date,
                                 source, library, notes])

                if i % 100 == 0:
                    print(filename + ": " + str(i) + " documents processed")


def get_title(record):
    # pymarc has a title() method that is similar to this, but it doesn't
    # concatenate subtitle and title properly
    if '245' in record and 'a' in record['245']:
        title = clean(record['245']['a'])
        if 'b' in record['245']:
            title += ' ' + clean(record['245']['b'])
        return title
    else:
        return None


def clean(element, is_author=False):
    if element is None or not element.strip():
        return None
    else:
        element = element.strip()

        for character in [',', ';', ':', '/']:
            if element[-1] == character:
                return element[:-1].strip()

        if not is_author and element[-1] == '.':
            # don't strip trailing periods from author names
            return element[:-1].strip()

        return element.strip()


if __name__ == '__main__':
    main()
