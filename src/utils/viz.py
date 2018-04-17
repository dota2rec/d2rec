import matplotlib
import matplotlib.mlab as mlab
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np

def cdf_plot(x, bins=10, xlabel='Similarity', name='cdf.pdf'):
    mu = np.mean(x)
    sigma = np.std(x)

    # the histogram of the data
    n, bins, patches = plt.hist(x, bins, normed=1, facecolor='blue', alpha=0.5)

    # add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, y, 'r--')
    plt.xlabel('Similarity')
    plt.ylabel('Cumulative Probability')
    plt.title(r' CDF: mu=' + str(mu) + ', sigma=' + str(sigma))

    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    #plt.show()
    plt.savefig(name, format='pdf')
    plt.clf()

def bar_plot(x, y, width=0.1, name='bar.pdf'):
    plt.bar(x, y, width, align='center')
    plt.savefig(name, format='pdf')
    plt.clf()
