import scrapy
from fantasy_football_scraper.items import Player
from bs4 import BeautifulSoup


class DepthChartSpider(scrapy.Spider):
    # identifies the spider
    name = "depth_charts"

    def start_requests(self):
        urls = [
            "http://www.seahawks.com/team/depth-chart",
            "http://www.dallascowboys.com/team/depth-chart",
            "http://www.patriots.com/schedule-and-stats/depth-chart"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

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
        player["team_name"] = get_team_name(response.request.url)
        return player


def get_team_name(url):
    return url.split(".")[1]