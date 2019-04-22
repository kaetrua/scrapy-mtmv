# -*- coding: utf-8 -*-
import scrapy


class MvSpider(scrapy.Spider):
    name = 'mv'
    allowed_domains = ['mtime.com']
    start_urls = ['http://mtime.com/']

    def parse(self, response):
        pass
