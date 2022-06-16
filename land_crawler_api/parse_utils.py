from collections import namedtuple
from itertools import chain
import csv
import re


def csv_parser(fname, *, encoding='utf8', delimiter=',', quotechar='"', include_header=False):
    with open(fname, encoding=encoding) as f:
        reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
        # skip chinese header
        next(f)
        # skip english header or not
        if not include_header:
            next(f)
        yield from reader


def complete_field_names(fname):
    reader = csv_parser(fname, include_header=True)

    # last 5 is empty, fix it
    header = next(reader)
    header = header[:-5]

    # turn it to valid name
    fields = []
    for field in header:
        field = field.lower()
        field = field.replace(' ', '_').replace('-', '_').replace('/', '_').replace('(', '_').replace(')', '_')
        field = re.sub(r'_+', r'_', field)
        fields.append(field)
    fields += ("main_building_area", "auxiliary_building_area", "balcony_area", "elevator", "transfer_number")
    return fields


def create_named_tuple_class(fname, class_name):
    fields = complete_field_names(fname)
    return namedtuple(class_name, fields)


def iter_file(fname, class_name):
    nt_class = create_named_tuple_class(fname, class_name)
    reader = csv_parser(fname)
    for row in reader:
        yield nt_class(*row)


def iter_combined_files(fnames, class_name):
    nt_class = create_named_tuple_class(fnames[0], class_name)
    rows = chain.from_iterable(csv_parser(fname) for fname in fnames)
    for row in rows:
        yield nt_class(*row)


if __name__ == "__main__":
    # test
    import constants
    from constants import file_dir, fnames, land_class_name
    from itertools import islice

    # checker fields
    csv_parser(constants.fname_a)
    print('fields')
    print(complete_field_names(constants.file_dir + '/' + constants.fname_a))
    print('--------')

    # see iterator run correctly or not
    fpaths = [f'{file_dir}/{fname}' for fname in fnames]
    files_iterator = iter_combined_files(fpaths, land_class_name)
    # 台北
    sample_a = next(islice(files_iterator, 10, 11))
    print('sample taipei')
    print(sample_a)
    print('--------')
    # 台中
    print('sample taichung')
    sample_b = next(islice(files_iterator, 6000, 6001))
    print(sample_b)
    print('--------')
