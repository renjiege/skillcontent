#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-09-04 00:13:16
# Project: careerlink

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
         'itag': 'v2'
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.careerlink.vn/en/quick-job-search', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            match = re.match(r"https://www.careerlink.vn/en/category/.*", each.attr.href, re.U)
            if match:
                self.crawl(each.attr.href, callback=self.search_page)

    @config(age=10 * 24 * 60 * 60)
    def search_page(self, response):

        page_num = []
        for each in response.doc('a[href^="http"]').items():
            match = re.match(r"https://www.careerlink.vn/en/category/.*headline&page=(\d+)", each.attr.href, re.U)
            if match:
                page_num.append(match.group(1))
             
        page_num = list(map(int, page_num))
        link = response.url + '?view=headline&page='
        print(page_num)
        if page_num:
            for each in range(1, max(page_num)+1):
                page = link + str(each)
                self.crawl(page, callback=self.job_list_page)
        else: 
            self.crawl(response.url, callback=self.job_list_page)
        
    @config(age=10 * 24 * 60 * 60)
    def job_list_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            match = re.match(r"https://www.careerlink.vn/en/job/.*", each.attr.href, re.U)
            if match:
                self.crawl(each.attr.href, callback=self.detail_page)        
    
    @config(priority=2)
    def detail_page(self, response):
        match = re.search(r"Career Level:(.*?)</li>", response.text, re.S)
        career_lvel = re.sub(r"[\n\t\s]*", "", match.group(1))
        
        company = response.doc('ul.list-unstyled.critical-job-data > li:nth-of-type(1) > a.text-accent > span > span').text()  
        
        location = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(3) > ul').text()
        if not location:
            location = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(4) > ul').text()
        
        category1 = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(1) > ul > li:nth-of-type(1) > a > span').text()
        category2 = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(1) > ul > li:nth-of-type(2) > a > span').text()
        category3 = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(1) > ul > li:nth-of-type(3) > a > span').text()
        educ_required = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(4) > span').text()
        experience = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(5) > span').text()
        type = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(6) > span').text()
        
        if not category1:
            category1 = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(2) > ul > li:nth-of-type(1) > a > span').text()   
            category2 = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(2) > ul > li:nth-of-type(2) > a > span').text() 
            category3 = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(2) > ul > li:nth-of-type(3) > a > span').text() 
            educ_required = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(5) > span').text()
            experience = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(6) > span').text()
            type = response.doc('div.job-data > ul:nth-of-type(2) > li:nth-of-type(7) > span').text()
          
        return {
            "career_lvel": career_lvel,
            "category1": category1,
            "category2": category2,
            "category3": category3,
            "company": company,
            "title": response.doc('h1 > span').text(),
            "educ_req": educ_required,
            "experience": experience,
            "type": type,
            "location": location, 
            "requirement": response.doc('div.job-data > div:nth-of-type(3) > p').text(),
            "description": response.doc('div.job-data > div:nth-of-type(2) > p').text(),
        }
