import sys
import re
from retrievetrainingdata import buidTrainingSet as build_training


def create_parser():
    pass


def main(args):
    training_data = build_training("corpus.csv", "tweetDataFile.csv")
    pass


if __name__ == '__main__':
    main(sys.argv[1:])
