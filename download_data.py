import requests
import os
import sys


def download_data(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    elif not os.path.isdir(dir_path):
        print('Path should point to directory', file=sys.stderr)
        exit(1)

    urls = ['https://files.digital.nhs.uk/publication/3/9/dem-diag-ind-phe-may-2017.csv',
            'https://files.digital.nhs.uk/publicationimport/pub24xxx/pub24036/dem-diag-ind-phe-apr-2017.csv',
            'https://files.digital.nhs.uk/publication/p/q/dem-diag-ind-phe-jun-2017.csv',
            'https://files.digital.nhs.uk/publication/o/9/dem-diag-ind-phe-jul-20173.csv',
            'https://files.digital.nhs.uk/publication/g/g/dem-diag-ind-phe-aug-2017.csv',
            'https://files.digital.nhs.uk/publication/g/7/dem-diag-ind-phe-sep-2017.csv',
            'https://files.digital.nhs.uk/publication/1/f/dem-diag-ind-phe-oct-2017.csv',
            'https://files.digital.nhs.uk/publication/r/4/dem-diag-ind-phe-nov-2017.csv',
            'https://files.digital.nhs.uk/publication/8/h/dem-diag-ind-phe-dec-2017.csv',
            'https://files.digital.nhs.uk/publication/f/7/dem-diag-ind-phe-jan-2018.csv',
            'https://files.digital.nhs.uk/excel/4/0/dem-diag-ind-phe-feb-2018.csv',
            'https://files.digital.nhs.uk/9F/C6127E/dem-diag-ind-phe-Mar-2018.csv',
            'https://files.digital.nhs.uk/89/A5593C/dem-diag-ind-phe-Apr-2018.csv',
            'https://files.digital.nhs.uk/EB/7EA4A5/dem-diag-ind-phe-May-2018.csv',
            'https://files.digital.nhs.uk/30/534FE0/dem-diag-ind-phe-Jun-2018.csv',
            'https://files.digital.nhs.uk/86/4755A4/dem-diag-ind-phe-Jul-2018.csv']
    for url in urls:
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except requests.exceptions.RequestException as err:
            print('Failed to download %s: %s' % (url, err), file=sys.stderr)
            continue
        f_name = url.split('/')[-1]
        if os.path.exists(os.path.join(dir_path, f_name)):
            print('File with same name already exists: %s' % f_name)
            continue
        with open(os.path.join(dir_path, f_name), 'wb') as file:
            file.write(resp.content)
        print('File downloaded: %s' % url)


def main():
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
            download_data(sys.argv[1])
        else:
            print('Argument should be valid path and should point to directory')
    else:
        print('Path to directory should be specified by argument')


if __name__ == '__main__':
    main()
