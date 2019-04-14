import os.path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import manifold
from scipy.misc import imread
from glob import iglob


# glob is a Unix style pathname pattern expansion.
# It finds all path names matching a specified pattern according to the rules used by the Unix shell,
# returned results in
# arbitrary order. glob.glob(pathname) returns a possibly empty list of path names that match pathname, which must be a
# string containing a path specification.
# glob.iglob() returns an iterator yielding the same values as glob.glob() w/out storing them all simultaneously.

store = 'images'

image_data = []

# os module is for accessing the filesystem. To read or write files: open().
# os.path module implements some useful operations on pathnames. path parameters can be strings or bytes.
# os.path.join() function joins one or more path components intelligently.

for filename in iglob(os.path.join(store, '*.jpg')):
    image_data.append(imread(filename))
    # scipy.misc.imread() reads an image from a file as an array.
    # It uses the Python Imaging Library (PIL) to read an image. But PIL isn't compatible with Python 3+, so
    # make sure you have Pillow (forked version of PIL) for Python 3+.

image_np_orig = np.array(image_data)
image_np = image_np_orig.reshape(image_np_orig.shape[0], -1)


def plot_embedding(X, image_np_orig):
    # Rescale
    x_min, x_max = np.min(X,0), np.max(X,0)
    X = (X - x_min) / (x_max - x_min)
    # Plot images according to t-SNE position
    plt.figure()
    ax = plt.subplot(111)
    for i in range(image_np.shape[0]):
        imagebox = offsetbox.AnnotationBbox(
            offsetbox=offsetbox.OffsetImage(image_np_orig[i], zoom=.1),
            xy=X[i],
            frameon=False)
        ax.add_artist(imagebox)


print("Computing t-SNE embedding")
tsne = manifold.TSNE(n_components=2, init='pca')
X_tsne = tsne.fit_transform(image_np)

plot_embedding(X_tsne, image_np_orig)
plt.show()