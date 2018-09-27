import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os


def adjust_dates(data):
    """
    Convert all dates to datetime format.
    :param data: pd.DataFrame
    :return: pd.DataFrame
    """
    data['DATE'] = pd.to_datetime(data['ACH_DATE'], format='%d%b%Y', errors='coerce')
    mask = data['DATE'].isnull()
    data.loc[mask, 'DATE'] = pd.to_datetime(data[mask]['ACH_DATE'], format='%d-%b-%y', errors='coerce')
    data['ACH_DATE'] = data['DATE']
    data = data.drop(['DATE'], axis=1)
    return data


def dem_registered_vs_estimate(data, year=None, verbose=False):
    """
    Compare number of registered patients and estimated number of patients.
    :param data: pd.DataFrame
    :param year: year by which to select.
    :param verbose: if true output will be produced to console.
    :return:
    """
    if year is None:
        out_a = data.loc[data['MEASURE'] == 'DEMENTIA_REGISTER_65_PLUS', ['NAME', 'ORG_TYPE', 'ACH_DATE', 'VALUE']]
        out_b = data.loc[data['MEASURE'] == 'DEMENTIA_ESTIMATE_65_PLUS', ['NAME', 'ORG_TYPE', 'ACH_DATE', 'VALUE']]
    else:
        out_a = data.loc[(data['MEASURE'] == 'DEMENTIA_REGISTER_65_PLUS') & (data['ACH_DATE'].dt.year == year),
                         ['NAME', 'ORG_TYPE', 'ACH_DATE', 'VALUE']]
        out_b = data.loc[(data['MEASURE'] == 'DEMENTIA_ESTIMATE_65_PLUS') & (data['ACH_DATE'].dt.year == year),
                         ['NAME', 'ORG_TYPE', 'ACH_DATE', 'VALUE']]

    out_a = out_a.merge(out_b, left_on=['NAME', 'ACH_DATE', 'ORG_TYPE'], right_on=['NAME', 'ACH_DATE', 'ORG_TYPE'],
                        suffixes=['_REGISTER', '_ESTIMATE'])
    out_a = out_a.sort_values(['NAME', 'ACH_DATE'])
    if verbose:
        print(out_a.to_string())
    return out_a


def plot_reg_vs_est(data, regions=None):
    dup = data.groupby(['NAME', 'ACH_DATE', 'VALUE_REGISTER', 'VALUE_ESTIMATE'])['ORG_TYPE'].apply(
        lambda x: ', '.join(x.astype(str))).reset_index()
    data = dup
    data = data.loc[data['NAME'].isin(regions)]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    legend = []
    for name, group in data.groupby(['NAME', 'ORG_TYPE']):
        date = group['ACH_DATE'].dt.date.values
        date = [x.strftime("%b %Y") for x in date]
        register = group['VALUE_REGISTER'].values
        estimate = group['VALUE_ESTIMATE'].values
        p = ax.plot(date, register, lw=2)
        c = p[-1].get_color()
        ax.plot(date, estimate, ls='--', color=c)
        legend.append('{}, registered.\n{}'.format(name[0].title(), name[1].title()))
        legend.append('{}, estimated.\n{}'.format(name[0].title(), name[1].title()))
    ax.grid(ls='--')
    min_yt = min(ax.get_yticks())
    max_yt = max(ax.get_yticks())
    step = int((max_yt - min_yt) / 20)
    ax.set_yticks(np.arange(min_yt, max_yt, step))
    ax.autoscale(tight=True, axis='x')
    ax.tick_params(axis='both', labelsize=8)
    ax.tick_params(axis='x', labelrotation=90)
    ax.legend(legend, fontsize=7, bbox_to_anchor=(1, 1))
    ax.set_title('Registered vs estimated number of  patients', fontsize=10)
    fig.tight_layout()
    return fig


def dem_regions_by_date(data, date=None, verbose=False):
    if date is None:
        out = data.loc[
            (data['MEASURE'] == 'DEMENTIA_REGISTER_65_PLUS')]
    else:
        out = data.loc[(data['MEASURE'] == 'DEMENTIA_REGISTER_65_PLUS') & (data['ACH_DATE'] == date)]
    out = out.sort_value(['NAME', 'ACH_DATE'])
    if verbose:
        print(out.to_string())
    return out


def analyze_dem(data):
    data = data.groupby(['NAME', 'ORG_TYPE']).agg({'VALUE': [np.min, np.max, np.mean]})
    print(data.to_string())


def plot_by_regions(data, regions):
    dup = data.groupby(['NAME', 'ACH_DATE', 'VALUE'])['ORG_TYPE'].apply(
        lambda x: ', '.join(x.astype(str))).reset_index()
    data = dup
    data = data.loc[data['NAME'].isin(regions)]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    x_label = []
    y_vals = []
    date = 0
    for name, group in data.groupby(['NAME', 'ORG_TYPE']):
        date = group['ACH_DATE'].dt.date.values
        if date.shape[0] > 1:
            date = date[-1]
        register = group.loc[(group['ACH_DATE'] == date), 'VALUE'].values
        x_label.append("{}\n{}".format(name[0].title(), name[1].title()))
        y_vals.append(register[0])
    ax.bar(x_label, y_vals)
    ax.tick_params(axis='both', labelsize=8)
    ax.tick_params(axis='x', labelrotation=90)
    ax.grid(ls=':', alpha=0.5)
    ax.set_title('Number of registered patients by {}'.format(date), fontsize=10)
    fig.tight_layout()
    return fig


def plot_by_time(data, regions):
    dup = data.groupby(['NAME', 'ACH_DATE', 'VALUE'])['ORG_TYPE'].apply(
        lambda x: ', '.join(x.astype(str))).reset_index()
    data = dup
    data = data.loc[data['NAME'].isin(regions)]
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    legend = []
    for name, group in data.groupby(['NAME', 'ORG_TYPE']):
        date = group['ACH_DATE'].dt.date.values
        date = [x.strftime("%b %Y") for x in date]
        register = group['VALUE'].values
        ax.plot(date, register, lw=2)
        legend.append('{}\n{}'.format(name[0].title(), name[1].title()))
    ax.grid(ls='--')
    min_yt = min(ax.get_yticks())
    max_yt = max(ax.get_yticks())
    step = int((max_yt - min_yt) / 20)
    ax.set_yticks(np.arange(min_yt, max_yt, step))
    ax.autoscale(tight=True, axis='x')
    ax.tick_params(axis='both', labelsize=8)
    ax.tick_params(axis='x', labelrotation=90)
    ax.legend(legend, fontsize=7, bbox_to_anchor=(1, 1))
    ax.set_title('Number of registered patients', fontsize=10)
    fig.tight_layout()
    return fig


def combine_multiple_dataframes(data):
    """
    Combines multiple DataFrames in one without duplicates.
    :param data: list of DataFrames objects.
    :return: DataFrame object.
    """
    data = pd.concat(data, ignore_index=True)
    data = adjust_dates(data)
    data = data.drop_duplicates(['NAME', 'ORG_TYPE', 'ACH_DATE', 'MEASURE']).reset_index(drop=True)
    data = data.sort_values(['NAME', 'ACH_DATE'])

    return data


def main():
    data = None
    date = None
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            data = [pd.read_csv(os.path.join(sys.argv[1], x))
                    for x in os.listdir(sys.argv[1]) if x.endswith('.csv')]
            if len(data) == 0:
                sys.exit(0)
        else:
            print("Path should point to directory with files")
            exit(1)
    else:
        print('Directory must be specified by command line argument')
        exit(1)
    data = combine_multiple_dataframes(data)
    dt = dem_regions_by_date(data)
    dt = dt.sort_values(['NAME', 'ACH_DATE'])
    dt.to_csv('tmp/dem_reg_2016-2018.csv')
    # analyze_dem(data)
    regions = list(dt.loc[data['ORG_TYPE'] == 'PHE_CENTRE', 'NAME'].unique())
    fig = plot_by_regions(dt, regions=regions)
    fig.savefig('tmp/by_regions.png')
    fig = plot_by_time(dt, ['ENGLAND'])
    fig.savefig('tmp/by_time.png')
    dt = dem_registered_vs_estimate(data, 2017)
    dt = dt.sort_values(['NAME', 'ACH_DATE'])
    dt.to_csv('tmp/dem_rev_vs_est_2107.csv')
    fig = plot_reg_vs_est(dt, regions=['WEST MIDLANDS'])
    fig.savefig('tmp/deg_reg_vs_est.png')
    plt.show()


if __name__ == '__main__':
    main()
