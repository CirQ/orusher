#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2018-03-19 21:04:12

from multiprocessing.dummy import Pool

from .browser import OWhatBrowser

class OWhatRusher(object):
    def __init__(self, n):
        self.n = n
        self.pool = Pool(n)

    def run(self):
        def wrapper():
            OWhatBrowser().run()
        for _ in range(self.n):
            self.pool.apply_async(wrapper)
        self.pool.close()
        self.pool.join()


if __name__ == '__main__':
    OWhatRusher(2).run()
