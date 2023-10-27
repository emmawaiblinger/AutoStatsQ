import logging
import os
import numpy as num
import matplotlib.pyplot as plt
from pyrocko import gmtpy


def gmtplot_catalog_azimuthal(catalog, mid_point, dist, outfile, bin_width):
    """
    Plot events of catalog on map

    :param catalog: event catalog in pyrocko format
    :param mid_point: centre of map
    :param dist: max. distance in degrees
    """
    gmt = gmtpy.GMT(config={'MAP_GRID_PEN_PRIMARY': '0.1p',
                            'MAP_GRID_PEN_SECONDARY': '0.1p',
                            # 'MAP_GRID_PEN_TERTIARY': '0.001p',
                            'MAP_FRAME_TYPE': 'fancy',
                            # 'GRID_PEN_PRIMARY': '0.01p',
                            # 'GRID_PEN_SECONDARY': '0.01p',
                            'FONT_ANNOT_PRIMARY': '14p,Helvetica,black',
                            'FONT_ANNOT_SECONDARY': '14p,Helvetica,black',
                            'FONT_LABEL': '14p,Helvetica,black',
                            'PS_MEDIA': 'Custom_%ix%i' % (20*gmtpy.cm, 20*gmtpy.cm)})
    gmt.psbasemap(
                  R='0/360/-90/0',
                  J='S0/-90/90/6i',
                  B='xa%sf%s' % (bin_width*2, bin_width))
    gmt.pscoast(
                R='g',
                J='E%s/%s/%s/6i' % (mid_point[1], mid_point[0], dist),
                D='c',
                G='darkgrey')
    gmt.psbasemap(
                  R='g',
                  J='E0/-90/%s/6i' % dist,
                  B='xg%s' % bin_width)
    gmt.psbasemap(
                  R='g',
                  J='E0/-90/%s/6i' % dist,
                  B='yg%s' % bin_width)
    gmt.psxy(R='0/360/-90/0',
             J='E%s/%s/%s/6i' % (mid_point[1], mid_point[0], dist),
             in_columns=([ev.lon for ev in catalog],
                         [ev.lat for ev in catalog]),
             G='red',
             S='a12p')
    gmt.save(outfile)
    logging.info('saved %s' % outfile)


def plot_catalog_hist(catalog, dist_array, mean_wedges_mp, bins_hist,
                      data_dir, min_mag, d, bin_width, no_bins,
                      plot_wedges_vs_dist=True,
                      plot_wedges_vs_magn=True,
                      full_cat=True):
    """
    Plot histogram showing number of earthquakes in each 15deg wedge
    """

    mean_dists = num.mean(dist_array, axis=1)
    fig, ax1 = plt.subplots()
    ax1.hist(mean_wedges_mp, bins=bins_hist, color='lightgrey')
    ax1.set_xlabel(str(bin_width) + r'$^\circ$' + ' backazimuth bins',
                   fontsize=10)
    ax1.set_ylabel('Number of events in catalog', fontsize=10)
    ax1.set_xlim((0, no_bins))
    # ax1.set_ylim((0.1, 100))
    # ax1.set_yscale('log', nonposy='clip')
    ax1.tick_params(axis='both', which='major', labelsize=8)

    if plot_wedges_vs_dist is True:
        '''
        Plot distance along with frequency
        '''
        ax2 = ax1.twinx()
        ax2.plot(mean_wedges_mp+0.5, mean_dists/1000, 'r.')
        ax2.tick_params('y', colors='r')
        ax2.set_ylabel('Distance (km)', color='r', fontsize=10)
        ax2.set_ylim((0, 30000))
        ax2.tick_params(axis='both', which='major', labelsize=8)

    if plot_wedges_vs_magn is True:
        '''
        Plot magnitude along with frequency
        '''
        ax3 = ax1.twinx()
        if plot_wedges_vs_dist is True:
            ax3.spines['right'].set_position(('axes', 1.2))
        ax3.plot(mean_wedges_mp+0.5, [ev.magnitude for ev in catalog], 'b.')
        ax3.tick_params('y', colors='b')
        ax3.set_ylim(min_mag-0.2, 10)
        ax3.set_ylabel('Magnitude '+r'$(M_W)$', color='b')
        ax3.tick_params(axis='both', which='major', labelsize=8)

    plt.tight_layout()

    if full_cat is True:
        plt.savefig(os.path.join(data_dir,
                    'results/catalog/cat_hist_magn_dist_%s.png' % d))
    else:
        plt.savefig(os.path.join(data_dir,
                    'results/catalog/cat_hist_magn_dist_%s_subset.png' % d))
    plt.close()


def plot_distmagn(dist_array, catalog, data_dir, d, full_cat):
    ''' Plot distance vs. magnitude for full downloaded
    catalog or subsets.'''

    mean_dists = num.mean(dist_array, axis=1)
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(mean_dists/1000, [ev.magnitude for ev in catalog], '.')
    ax.set_xlabel('Distance '+r'$(km)$', fontsize=10)
    ax.set_ylabel('Magnitude '+r'$(M_W)$', fontsize=10)
    ax.tick_params(axis='both', which='major', labelsize=8)
    plt.tight_layout()
    if full_cat is True:
        plt.savefig(os.path.join(data_dir,
                    'results/catalog/cat_dist_vs_magn_%s.png' % d))
    else:
        plt.savefig(os.path.join(data_dir,
                    'results/catalog/cat_dist_vs_magn_%s_subset.png' % d))
    plt.close()
