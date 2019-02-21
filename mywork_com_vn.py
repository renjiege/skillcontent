#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-10-29 19:37:36
# Project: mywork_com_vn

from pyspider.libs.base_handler import *
import re
 
class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://mywork.com.vn/', callback=self.option_page)
        
    @config(age=10 * 24 * 60 * 60)
    def option_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            match = re.match(r"https://mywork.com.vn/tuyen-dung/dia-diem.*", each.attr.href, re.U)
            if match:
                self.crawl(each.attr.href, callback=self.index_page)
        
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):   
        url = response.url
        loc = re.search(r'dia-diem/(\d+)', url).group(1)
        total_pages = re.search(r'total_pages\":(\d+)', response.text).group(1)
        for num in range(1, int(total_pages)+1):
            url = f'https://mywork.com.vn/tuyen-dung/dia-diem/{loc}/quang-binh.html/trang/{num}?locations={loc}'
            self.crawl(url, callback=self.list_page)
                
    @config(age=10 * 24 * 60 * 60)
    def list_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            match = re.match(r"https://mywork.com.vn/tuyen-dung/viec-lam/\d.*", each.attr.href, re.U)
            if match:
                self.crawl(each.attr.href, callback=self.detail_page)
                      
    @config(priority=2)
    def detail_page(self, response):
        return {
            "title": response.doc('h1.main-title > span').text(),
            "educ_req": response.doc('div.mw-box-item.job_detail_general > div:first-child > p:nth-of-type(2)').text(),
            "experience": response.doc('div.mw-box-item.job_detail_general > div:first-child > p:first-child').text(),
            "type":response.doc('div.mw-box-item.job_detail_general > div:nth-of-type(2) > p:first-child').text(),
            "category1": response.doc('div.mw-box-item.job-cat > span:nth-of-type(1)').text(),
            "category2": response.doc('div.mw-box-item.job-cat > span:nth-of-type(2)').text(),
            "category3": response.doc('div.mw-box-item.job-cat > span:nth-of-type(3)').text(),
            "location1": response.doc('div.row.row-standard > div:nth-of-type(2) > p:nth-of-type(1) > span:nth-of-type(1) > a').text(),
            "location2": response.doc('div.row.row-standard > div:nth-of-type(2) > p:nth-of-type(1) > span:nth-of-type(2) > a').text(),
            "location3": response.doc('div.row.row-standard > div:nth-of-type(2) > p:nth-of-type(1) > span:nth-of-type(3) > a').text(),
            "location4": response.doc('div.row.row-standard > div:nth-of-type(2) > p:nth-of-type(1) > span:nth-of-type(4) > a').text(),
            "location5": response.doc('div.row.row-standard > div:nth-of-type(2) > p:nth-of-type(1) > span:nth-of-type(5) > a').text(),
            "location6": response.doc('div.row.row-standard > div:nth-of-type(2) > p:nth-of-type(1) > span:nth-of-type(6) > a').text(),
            "expire_date": response.doc('div.row.row-standard > div:nth-of-type(2) > p:nth-of-type(3) > span').text(),
            "post_date": response.doc('div.content.text-center > p:nth-of-type(2)').text(),
            "company": response.doc('h2.desc-for-title > span:nth-of-type(1)').text(),
            "description":response.doc("div.col-left > div:first-child > div:nth-of-type(3)").text(),
            "requirement": response.doc("div.col-left > div:first-child > div:nth-of-type(5)").text(),

        }
    
