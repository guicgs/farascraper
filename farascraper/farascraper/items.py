# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class ActiveForeignPrincipalItem(scrapy.Item):
    url = scrapy.Field()
    foreign_principal = scrapy.Field()
    fp_reg_date = scrapy.Field()
    address = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()
    registrant = scrapy.Field()
    reg_num = scrapy.Field()
    exhibits = scrapy.Field()
    reg_date = scrapy.Field()
