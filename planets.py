# this program is setup to use data from the NASA Exoplanet Archive
# you can find the data at the link below. When downloading be sure to include
# the options for 'all columns' and 'all rows'
# http://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=planets

import errno
import csv
import os
import sys

TMP_FILENAME = 'tmp.csv'
logging = False

def log(msg):
    if logging:
        print(msg)

def cleanup():
    try:
        os.remove(TMP_FILENAME)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

def pretty_print(data):
    for category in data:
        print('{} (count: {}):'.format(category, data[category]['count']))
        for item in data[category]:
            if item == 'count':
                continue
            print('  {}: {:0.4f}'.format(item, data[category][item]))

        print()

def load_csv(filename):
    log('loading data from {}'.format(filename))

    seen_headers = False
    data_point = None
    discovery_methods = set()
    tmpfile = open(TMP_FILENAME, 'w')
    with open(filename) as infile:
        for line in infile:
            if line[0] == '#':
                continue

            if not seen_headers:
                seen_headers = True

                # remove end of line character
                line = line[:-1]
                # create lookup dict for headers
                headers = {}
                for i, header in enumerate(line.split(',')):
                    headers[header] = i
            else:
                tmpfile.write(line)

                data_point = line.split(',')[headers['pl_discmethod']]
                if data_point:
                    discovery_methods.add(data_point)

    tmpfile.close()
    log('finished loading data')
    log('  tmp file created at {}'.format(TMP_FILENAME))
    log('  the headers and discovery methods were parsed')

    return (headers, discovery_methods)

def avg_data_by_bucket(headers, buckets, params):
    log('averaging data in the following buckets: {}'.format(buckets))
    log('  on the following params: {}'.format(params))

    # initialize our data structure
    results = {}
    results_count = {}
    for bucket in buckets:
        results[bucket] = {}
        results_count[bucket] = {}
        results[bucket]['count'] = 0
        for param in params:
            results[bucket][param] = 0
            results_count[bucket][param] = 0

    data_point = None
    line_split = None
    bucket = None
    with open(TMP_FILENAME) as infile:
        for line in infile:
            line_split = line.split(',')
            bucket = line_split[headers['pl_discmethod']]
            if bucket:
                results[bucket]['count'] += 1
            for param in params:
                data_point = line_split[headers[param]]
                if data_point and bucket:
                    results[bucket][param] += float(data_point)
                    results_count[bucket][param] += 1

    for param in params:
        results[bucket][param] = results[bucket][param] / results_count[bucket][param]

    return results

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        try:
            flag = sys.argv[2]
        except:
            flag = None
    except:
        print('Usage:')
        print('  python3 planets.py <path to data> <options>')
        print('Options:')
        print('  -v detailed output')
        sys.exit(1)

    if flag == '-v':
        logging = True

    headers, discovery_methods = load_csv(filename)

    results = avg_data_by_bucket(headers, discovery_methods, [
        'pl_orbper',
        'pl_massj',
        'pl_dens'
    ])

    pretty_print(results)

    cleanup()
