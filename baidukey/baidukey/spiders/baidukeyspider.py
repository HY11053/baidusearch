# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from baidukey.items import BaidukeyItem


class BaidukeyspiderSpider(scrapy.Spider):
    name = 'baidukeyspider'
    allowed_domains = ['baidu.com']
    inputerkey=input('请输入要抓取的关键词相关搜索')
    keywords={"wd":inputerkey}
    mkeywords={"word":inputerkey}
    start_urls = [
        "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&"+parse.urlencode(keywords)+"&rsv_pq=e360b0570000a1df&rsv_t=d4a4BZr%2BOrwigVViSNsZ7xZPxP7rmun2djAgvPiU0JYtV%2BcEKEiV6f5LK90&rqlang=cn&rsv_enter=1&rsv_sug3=26&rsv_sug1=44&rsv_sug7=101&rsv_sug2=0&inputT=10619&rsv_sug4=10619",
       # "https://www.baidu.com/from=844b/s?"+parse.urlencode(mkeywords)+"&sasub=gh_icon20180608&ts=7664786&t_kt=0&ie=utf-8&fm_kl=021394be2f&rsv_iqid=1259112935&rsv_t=9db7FL7iPVF14yxGOedP%252FYSXBfBz%252FlVZYKnA7t5%252Bp2K9Fc7YPH8LkCLe0A&sa=ib&ms=1&rsv_pq=1259112935&rsv_sug4=3672&tj=1&inputT=2461&ss=100"

    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parse)
    def parse(self, response):
        item=BaidukeyItem()
        for keyword in response.xpath('//div[@id="rs"]/table/tr/th/a/text()').extract():
            if(keyword.find('干洗店') != -1or keyword.find('洗衣店')!=-1):
                item['keywords']=keyword
                item['types']='百度'
                item['status']=0
            yield item
        for href in response.xpath('//div[@id="rs"]/table/tr/th/a/@href').extract():
            #print(href)
            fullhref=response.urljoin(href)
            yield scrapy.Request(url=fullhref,callback=self.parse)


