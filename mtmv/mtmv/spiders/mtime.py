from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from ..items import MtimeMovieItem, ImageItem

class MtimeSpider(BaseSpider):
    name = "mtime"
    allowed_domains = ["movie.mtime.com/"]

    start_urls = [
        # "http://movie.mtime.com/movie/search/section/",
        "http://movie.mtime.com/31889/"
    ]

    # 定义需要爬取页面的起始和结束id///10000, 263780
    for num in range(50000, 50006):
        start_urls.append("http://movie.mtime.com/{0}/".format(num))

    def parse(self, response):
        data = response.xpath('//div[@class="db_topcont"]')
        datarate = response.xpath('//div[@class="db_i_comcont"]')
        movie_item = MtimeMovieItem()
        movie_title = response.xpath('//title/text()').extract()[0]
        if "你要访问的页面不存在" not in movie_title:
            if len(data.xpath('//div[@class="clearfix"]/h1/text()').extract()) <= 0:
                movie_item['movie_name'] = 'N/A'
            else:
                movie_item['movie_name'] = data.xpath('//div[@class="clearfix"]/h1/text()').extract()[0]
            if len(data.xpath('//p[@class="db_year"]/a/text()').extract()) <= 0:
                     movie_item['movie_yeat'] = 'N/A'
            else:
                     movie_item['movie_year'] = data.xpath('//p[@class="db_year"]/a/text()').extract()[0]
            if len(data.xpath('//p[@class="db_enname"]/text()').extract()) <= 0:
                     movie_item['movie_enname'] = 'N/A'
            else:
                     movie_item['movie_enname'] = data.xpath('//p[@class="db_enname"]/text()').extract()[0]
            if len(data.xpath('//div[@class="otherbox __r_c_"]/a/text()').extract()) <= 0:
                     movie_item['movie_type'] = 'N/A'
            else:
                     movie_item['movie_type'] = data.xpath('//div[@class="otherbox __r_c_"]/a/text()').extract()[0]
            if len(data.xpath('//div[@class="base_r"]/div/dl/dd[4]/a/text()').extract()) <= 0:

                     movie_item['movie_country'] = 'N/A'
            else:
                     movie_item['movie_country'] = \
                         data.xpath('//div[@class="base_r"]/div/dl/dd[4]/a/text()').extract()[0]

            if len(datarate.xpath('//span[@class="db_point ml6"]/text()').extract()) <= 0:
                movie_item['movie_rate'] = '0.0'
            else:
                movie_item['movie_rate'] = \
                    datarate.xpath('//span[@class="db_point ml6"]/text()').extract()[0]


            if len(data.xpath('//div[@class="base_r"]/div/dl/dd/a/text()').extract()) <= 0:
                movie_item['movie_director'] = 'N/A'
            else:
                movie_item['movie_director'] = data.xpath('//div[@class="base_r"]/div/dl/dd/a/text()').extract()[0]


            movie_item['mtime_url'] = response.url
            return movie_item


class MtimePhotoSpider(BaseSpider):
    name = "mPicture"
    allowed_domains = ["movie.mtime.com/"]

    start_urls = [
        # "http://movie.mtime.com/movie/search/section/",
        "http://movie.mtime.com/31889/"
    ]

    # 定义需要爬取页面的起始和结束id
    for num in range(31889, 32889):
        start_urls.append("http://movie.mtime.com/{0}/".format(num))

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        imgs = hxs.select('//img/@src').extract()
        item = ImageItem()
        item['image_urls'] = imgs
        return item
