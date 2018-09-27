import pandas as pd
import datetime
import sys
import os


def adjust_dates(data):
    data['DATE'] = pd.to_datetime(data['ACH_DATE'], format='%d%b%Y', errors='coerce')
    mask = data['DATE'].isnull()
    data.loc[mask, 'DATE'] = pd.to_datetime(data[mask]['ACH_DATE'], format='%d-%b-%y', errors='coerce')
    data['ACH_DATE'] = data['DATE']
    data = data.drop(['DATE'], axis=1)
    return data


def dem_all_regions_by_date(data, date=None):
    """
    Outputs number of patients with registered dementia for all region for given date
    :param data: pandas DataFrame object.
    :param date: date of the record in dd/mm/yyyy format.
    :return:
    """
    data = adjust_dates(data)
    if date is None:
        out = data.loc[
            (data['MEASURE'] == 'DEMENTIA_REGISTER_65_PLUS')]
    else:
        out = data.loc[
            (data['MEASURE'] == 'DEMENTIA_REGISTER_65_PLUS') &
            (data['ACH_DATE'] == date)]

    out = pd.DataFrame(out[['NAME', 'MEASURE', 'ACH_DATE', 'VALUE']])
    out.columns = ['Region', 'Category', 'Date', 'num of patients']
    formatters = {'Region': '{{:<{}s}}'.format(out['Region'].str.len().max()).format}
    print(out.to_string(index=False, justify='left', formatters=formatters))


def main():
    data = None
    date = None
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
            data = pd.read_csv(sys.argv[1])
        else:
            print("Path should point to existing file")
            exit(1)
    else:
        print('File must be specified by command line argument')
        exit(1)

    if len(sys.argv) > 2:
        try:
            date = datetime.datetime.strptime(sys.argv[2], '%d/%m/%Y')
        except ValueError:
            date = None
            print('Date should be in %d/%m/%Y format')
            exit(1)

    dem_all_regions_by_date(data, date)


if __name__ == '__main__':
    main()
