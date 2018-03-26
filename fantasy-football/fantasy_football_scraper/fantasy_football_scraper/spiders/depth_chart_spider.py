import scrapy
from fantasy_football_scraper.items import Player
from bs4 import BeautifulSoup


class DepthChartSpider(scrapy.Spider):
    # identifies the spider
    name="depth_charts"
    curr_team = ""

    def start_requests(self):
        urls = [
            "http://www.seahawks.com/team/depth-chart"
        ]

        for url in urls:
            self.get_team_name(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def get_team_name(self, url):
        self.curr_team = url.split(".")[1]

    def parse(self, response):
        player = Player()
        row = {}

        items = response.xpath('//tbody/tr[contains(@class, "field_collection_item")]')
        for item in items.extract():
            result = BeautifulSoup(item, "lxml")
            position = result.body.find("div", attrs={"class": "field__item"}).text
            names = result.body.find_all("a", attrs={"class": "player"})

            player_names = []

            for name in names:
                player_names.append(name.text)

            if position in row.keys():
                position += "2"
            row[position] = player_names

        player["row"] = row
        player["team_name"] = self.curr_team
        return player