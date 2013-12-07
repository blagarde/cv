#!/usr/bin/env python
from utils import ximages
from learning import SVMClassifier, Dataset, Observation
from argparse import ArgumentParser


class ImageObservation(Observation):
    '''An observation the _data_ attribute of which is a cv2 image'''
    def as_vector(self):
        return self.data.ravel()


def get_image_observations(folders):
    for f in folders:
        for im in ximages(f):
            yield ImageObservation(im, f)


if __name__ == "__main__":
    parser = ArgumentParser(description="Train an image classifier")
    parser.add_argument('folders', type=str, nargs='+', help="List of folder paths, each containing a specific category of image. The format/size of the images must be consistent.")
    parser.add_argument('-v', '--validate', type=int, default=None, metavar='N_FOLDS',
        help="Instead of creating a model, get the classifier's precision using K-fold validation (supply the number of folds).")
    parser.add_argument('-o', '--output', type=str, default='model.pkl', metavar='OUTPATH', help="Save model to a file.")
    args = parser.parse_args()
    images = get_image_observations(args.folders)
    dataset = Dataset(images)
    classifier = SVMClassifier(dataset)
    if args.validate is not None:
        print "K-fold validation..."
        precision = classifier.validate(n_folds=args.validate, verbose=True)
        raise SystemExit("Precision:", precision)
    classifier.train()
    classifier.dump(args.output)
