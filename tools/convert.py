#!/usr/bin/env python3
"""
Base code for this script was taken from https://github.com/DavidChouinard/mrc_to_csv
Code was modified to make it work with python3
"""
import csv
import os

from pymarc import MARCReader


def main():
    """ Main function
    """
    for filename in os.listdir('../data/mrc/'):
        if os.path.isdir('data/mrc/' + filename) or filename[0] == '.':
            continue

        with open('../data/csv/' + os.path.splitext(filename)[0] + '.csv', 'wb') as input_file, \
                open('../data/mrc/' + filename, 'rb') as output_file:

            reader = MARCReader(output_file)
            writer = csv.writer(input_file)
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
    """ Get proper title
    pymarc has a title() method that is similar to this, but it doesn't
    concatenate subtitle and title properly
    """
    if '245' in record and 'a' in record['245']:
        title = clean(record['245']['a'])
        if 'b' in record['245']:
            title += ' ' + clean(record['245']['b'])
        return title

    return None


def clean(element, is_author=False):
    """ Clean records from punctuation marks

    :param element:
    :param is_author:
    :return:
    """
    if element is not None and element.strip():
        element = element.strip()

        for character in [',', ';', ':', '/']:
            if element[-1] == character:
                return element[:-1].strip()

        if not is_author and element[-1] == '.':
            # don't strip trailing periods from author names
            return element[:-1].strip()

        return element.strip()

    return None


if __name__ == '__main__':
    main()
