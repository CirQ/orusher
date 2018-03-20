#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: cirq
# Created Time: 2018-03-17 18:23:56

import time

from selenium.common.exceptions import *
from splinter.browser import FirefoxWebDriver
from splinter.exceptions import ElementDoesNotExist

from .config import *

# Splinter docs:
# http://splinter.readthedocs.io/en/latest/index.html

class ShareDict(dict):
    def __init__(self):
        super().__init__()

    def empty(self):
        return len(self) == 0


class OWhatBrowser(FirefoxWebDriver):

    share = ShareDict()

    def __init__(self):
        super().__init__()
        self.host = 'https://www.owhat.cn'
        self.sleeptime = 0.1

    def __not_selected(self):
        try:
            return not self.find_by_css('.btn-selected')
        except ElementDoesNotExist:
            return True

    def __add_to_share(self):
        share = OWhatBrowser.share
        btn = self.find_by_css('.btn-selected').first._element
        share['select_index'] = btn.get_attribute('selectindex')
        for txt in self.find_by_css('.pub_input'):
            ele = txt._element
            if ele.get_attribute('key') not in require_info:
                share['info_key'] = ele.get_attribute('key')
                share['info_value'] = ele.get_attribute('value')

    def __fill_blank(self):
        share = OWhatBrowser.share
        css_selector = '.pub_input[key={}]'.format(share['info_key'])
        self.find_by_css(css_selector)[0].fill(share['info_value'])
        css_selector = '.btn-select[selectindex="{}"]'.format(share['select_index'])
        self.find_by_css(css_selector)[0].click()

    def _login(self, un, pw):
        url = self.host + '/user/login.html'
        self.visit(url)
        self.find_by_id('mobile').fill(un)
        self.find_by_id('password').fill(pw)
        self.find_by_id('btn-login').click()

    def _book(self, tid, info):
        url = self.host + '/shop/shopdetail.html?id=' + str(tid)
        self.visit(url)
        btnType = self.find_by_id('btnType')
        while self.url == url:
            try:
                btnType.click()
            except ElementClickInterceptedException:
                time.sleep(self.sleeptime)
        for key, value in info.items():
            css_selector = '.pub_input[key={}]'.format(key)
            self.find_by_css(css_selector)[0].fill(value)

    def _buy(self):
        share = OWhatBrowser.share
        while share.empty() and self.__not_selected():
            time.sleep(self.sleeptime)
        if share.empty():
            self.__add_to_share()
        else:
            self.__fill_blank()
        self.find_by_css('.btn-buy')[0].click()
        btn = self.find_by_css('.btn-all')[0]
        while True:
            try:
                btn.click()
                break
            except ElementClickInterceptedException:
                time.sleep(self.sleeptime)

    def run(self):
        self._login(username, password)
        self._book(ticketid, require_info)
        self._buy()


if __name__ == '__main__':
    b = OWhatBrowser()
    b.run()
