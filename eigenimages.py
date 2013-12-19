#!/usr/bin/env python
import os
from sklearn.decomposition import PCA
from argparse import ArgumentParser
from learning import Dataset, Observation
from utils import ximages
import cv2


def write(img, path):
    cv2.imwrite(path, img)
    print "Wrote:", path


if __name__ == "__main__":
    parser = ArgumentParser(description="Applies PCA to an image dataset and outputs N images: projections of an image onto the first 1, 2, ..., N components.\
        The image that gets analysed is currently the first one in the dataset.")
    parser.add_argument('input', type=str, metavar='PATH', help="A folder containing images. The format/size of the images must be consistent.")
    parser.add_argument('-n', type=int, default=None, metavar='EIGENIMAGES', help="Number of output images (= number of eigenimages to extract.)")
    parser.add_argument('-o', '--output', type=str, default='pca_output', metavar='OUTPATH', help="Output folder.")
    args = parser.parse_args()

    images = (Observation(im, None) for im in ximages(args.input))
    dataset = Dataset(images)
    X = dataset.X()
    pca = PCA(n_components=args.n)
    pca.fit(X)
    
    h = w = 64
    eigenimages = pca.components_.reshape((args.n, h, w))
    mean = pca.mean_
    mod = pca.transform(X)
    rebuilt = mean + sum([k * ei for (k, ei) in zip(mod[0], pca.components_)])
    outpath = args.output
    if not os.path.exists(outpath):
        os.makedirs(outpath)
        print "Created:", outpath

    write(X[0].reshape(h, w), os.path.join(outpath, 'orig.ppm'))
    write(mean.reshape((h, w)), os.path.join(outpath, 'mean.ppm'))

    projected = mod[0]
    for i in range(len(eigenimages)):
        rebuilt = mean + sum([k * ei for (k, ei) in zip(projected[:i + 1], pca.components_[:i + 1])])
        path = os.path.join(outpath, str(i).zfill(4) + '.ppm')
        write(rebuilt.reshape(h, w), path)
