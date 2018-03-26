# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Player(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # player_heights = scrapy.Field()
    # player_positions = scrapy.Field()
    # player_years = scrapy.Field()
    # player_names = scrapy.Field()
    # position_names = scrapy.Field()
    team_name = scrapy.Field()
    row = scrapy.Field()