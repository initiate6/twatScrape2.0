#linkedin parser to get the juciey shit you know what I am talking about. 
#Script is dirty just the way you like it. 


import json

from scrapy.crawler import CrawlerProcess
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from scrapy import log, signals, Spider, Item, Field
from scrapy.settings import Settings
from twisted.internet import reactor

import re

global links
global words
global hash_tags
global dates

links = []
words = []
hash_tags = []
dates = []

class zSpider(Spider):
	name = "linkedout"
	allowed_domains = ["linkedin.com"]
	url = "<insert URL HERE>"
	start_urls = [url]

	def parse(self, response):
		#[u'Dallas, Texas']
		city_state = response.xpath('//*[@id="demographics"]/dd[1]/span/text()').extract()
		if city_state:
			for line in city_state:
				hash_tags.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))
					hash_tags.append(x.encode('ascii','ignore'))


		#Industry keywords
		industry = response.xpath('//*[@id="demographics"]/dd[2]/text()').extract()
		if industry:
			for line in industry:
				hash_tags.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))


		#Name
		name = response.xpath('//*[@id="name"]/text()').extract()
		if name:
			for line in name:
				hash_tags.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))
					hash_tags.append(x.encode('ascii','ignore'))


		#current work text 
		cur_work = response.xpath('//*[@id="topcard"]/div[1]/div/div/table/tbody/tr[1]/td/ol/li/span/a/text()').extract()
		if cur_work:
			for line in name:
				hash_tags.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))


		#Current work Link  
		cur_work_link = response.xpath('//*[@id="topcard"]/div[1]/div/div/table/tbody/tr[1]/td/ol/li/span/a/@href').extract()
		if cur_work_link:
			for line in cur_work_link:
				links.append(line.encode('ascii','ignore'))

		#Previous work text
		prev_work = response.xpath('//*[@id="topcard"]/div[1]/div/div/table/tbody/tr[2]/td/ol/li/a/text()').extract()
		if prev_work:
			for line in prev_work:
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))

		#Previous work link 
		prev_work_link = response.xpath('//*[@id="topcard"]/div[1]/div/div/table/tbody/tr[2]/td/ol/li/a/@href').extract()
		if prev_work_link:
			for x in prev_work_link:
				links.append(x.encode('ascii','ignore'))

		#Education text 
		edu = response.xpath('//*[@id="topcard"]/div[1]/div/div/table/tbody/tr[3]/td/ol/li/a/text()').extract()
		if edu:
			for line in edu:
				words.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))

		#Education link 
		edu_link = response.xpath('//*[@id="topcard"]/div[1]/div/div/table/tbody/tr[3]/td/ol/li/a/@href').extract()
		if edu_link:
			for x in edu_link:
				links.append(x.encode('ascii','ignore'))

		#Positions Text
		pos = response.css('.positions').xpath('.//p/text()').extract()
		if pos:
			for line in pos:
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))

		#Postion Titles
		pos_titles = response.css('.positions').css('.item-title').xpath('.//a/text()').extract()
		if pos_titles:
			for line in pos_titles:
				words.append(line.encode('ascii','ignore'))
				hash_tags.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))
			
		#Postion Title Links
		pos_titles_link = response.css('.positions').css('.item-title').xpath('.//a/@href').extract()
		if pos_titles_link:
			for x in pos_titles_link:
				links.append(x.encode('ascii','ignore'))

		#skillz 
		skillz = response.css('.skill').xpath('.//a').re(r'title="([^"]+)')
		if skillz:
			for line in skillz:
				words.append(line.encode('ascii','ignore'))
				hash_tags.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))	

		#Volunteer Description text
		vol = response.xpath('//*[@id="volunteering"]').xpath('.//p/text()').extract()
		if vol:
			for line in vol:
				for x in line.split():
					words.append(x.encode('ascii','ignore'))

		#Volunteer Titles text 
		vol_titles = response.xpath('//*[@id="volunteering"]').css('.item-title').xpath('.//text()').extract()
		if vol_titles:
			for line in vol_titles:
				words.append(line.encode('ascii','ignore'))
				hash_tags.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))

		#Volunteer Sub-Titles text 
		vol_subtitles = response.xpath('//*[@id="volunteering"]').css('.item-subtitle').xpath('.//text()').extract()
		if vol_subtitles:
			for line in vol_subtitles:
				for x in line.split():
					hash_tags.append(x.encode('ascii','ignore'))
					words.append(x.encode('ascii','ignore'))


		#Volunteer Sub-Titles links  
		vol_link = response.xpath('//*[@id="volunteering"]').css('.item-subtitle').xpath('.//@href').extract()
		if vol_link:
			for x in vol_link:
				links.append(x.encode('ascii','ignore'))

		#Education Titles text  
		edu_titles = response.css('.school').css('.item-title').xpath('.//text()').extract()
		if edu_titles:
			for line in edu_titles:
				words.append(line.encode('ascii','ignore'))
				hash_tags.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))


		#Education Titles links  
		edu_titles_link = response.css('.school').css('.item-title').xpath('.//@href').extract()
		if edu_titles_link:
			for x in edu_titles_link:
				links.append(x.encode('ascii','ignore'))


		#Education Sub-Titles text 
		edu_subtitles = response.css('.school').css('.item-subtitle').xpath('.//text()').extract()
		if edu_subtitles:
			for line in edu_subtitles:
				words.append(line.encode('ascii','ignore'))
				hash_tags.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))


		#Education Descriptions text 
		edu_desc = response.css('.school').css('.description').xpath('.//text()').extract()
		if edu_desc:
			for line in edu_desc:
				words.append(line.encode('ascii','ignore'))
				hash_tags.append(line.encode('ascii','ignore'))
				for x in re.split(' |/', line):
					words.append(x.encode('ascii','ignore'))


		#Groups text
		groups = response.css('.group').css('.item-title').xpath('.//text()').extract()
		if groups:
			for line in groups:
				for x in line.split():
					hash_tags.append(x.encode('ascii','ignore'))
					words.append(x.encode('ascii','ignore'))
		#Groups links
		group_link = response.css('.group').css('.item-title').xpath('.//@href').extract()
		if group_link:
			for x in group_link:
				links.append(x.encode('ascii','ignore'))

		#years
		years = response.xpath('//time/text()').re(r'([\d]+)')
		if years:
			for line in years:
				for x in line.split():
					dates.append(x.encode('ascii','ignore'))
					words.append(x.encode('ascii','ignore'))

		#months
		months = response.xpath('//time/text()').re(r'([^\d]+)')
		if months:
			for line in months:
				for x in line.split():
					dates.append(x.encode('ascii','ignore'))
					words.append(x.encode('ascii','ignore'))


settings = Settings()
settings.set('USER_AGENT', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.108 Safari/537.36')
settings.set('BOT_NAME', 'Something new')

crawler = CrawlerProcess(settings)

crawler.crawl(zSpider)
crawler.start()

#get uniq out of the string list
def uniq(tmp_listobj):
    listobj = []
    for l in tmp_listobj:
	l_tmp = l.lower()
	l_tmp2 = re.sub(r'\(|\)|,', '', l_tmp)
	l_tmp3 = re.sub(r'^[\s]*|$[\s]*', '', l_tmp2)
        listobj.append(l_tmp3)
    final = []
    small = []
    listobj.sort()
    temp = ""
    for item in listobj:
        if item != temp:
            if len(item) > 3:
                final.append(item)
                temp = item
	    else:
		small.append(item)
		temp = item  
    return small, final

link_small, clean_links = uniq(links)
words_small, clean_words = uniq(words)
hash_tags_small, clean_hash_tags = uniq(hash_tags)
dates_small, clean_dates = uniq(dates)

small = []
for x in link_small:
	small.append(x)
for x in words_small:
	small.append(x)
for x in hash_tags_small:
	small.append(x)
for x in dates_small:
	small.append(x)

clean_small, tmp = uniq(small)

print("\nlinks: %s\n\n" % clean_links)
print("\nwords: %s\n\n" % clean_words)
print("\nhash_tags: %s\n\n" % clean_hash_tags)
print("\ndates: %s\n\n" % clean_dates)
print("\nsmall: %s\n\n" % clean_small)
