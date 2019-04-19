#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import pickle


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('infile')
    args = parser.parse_args()

    with open(args.infile, 'rb') as fin:
        data = pickle.load(fin)

    for k in sorted(data):
        print('=' * 10, k, '=' * 10)
        print(data[k])
        print()
    

if __name__ == '__main__':
    main()

