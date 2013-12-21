#!/usr/bin/env python
import os
from sklearn.decomposition import PCA
from argparse import ArgumentParser
from learning import Dataset, Observation
from utils import ximages, write_to
import cv2


class Morpher(PCA):
    def __init__(self, images, *args, **kwargs):
        super(Morpher, self).__init__(*args, **kwargs)
        dataset = Dataset(images)
        X = dataset.X()
        self.fit(X)

    def rebuild(self, orig, n=None):
        h, w = orig.shape
        n = self.components_[0] if n is None else n
        mean = self.mean_
        projected = self.transform(orig.ravel())[0]
        img = mean
        for k, ei in zip(projected, self.components_):
            img += k * ei
            yield img.reshape(h, w)


if __name__ == "__main__":
    parser = ArgumentParser(description="Applies PCA to an image dataset and outputs N images: an input image's projections onto the first 1, 2, ..., N components.")
    parser.add_argument('image', type=str, help="The image to analyze.")
    parser.add_argument('inputfolder', type=str, help="A folder containing images. The format/size of the images must be consistent.")
    parser.add_argument('-n', type=int, default=None, help="Number of output images (= number of eigenimages to extract.)")
    parser.add_argument('-o', '--output', type=str, default='pca_output', metavar='OUTPATH', help="Output folder.")
    args = parser.parse_args()

    orig = cv2.imread(args.image, flags=cv2.CV_LOAD_IMAGE_GRAYSCALE)
    images = (Observation(im, None) for im in ximages(args.inputfolder, checksize=True))
    
    m = Morpher(images, n_components=args.n)
    write_to(m.rebuild(orig, n=args.n), args.output)
