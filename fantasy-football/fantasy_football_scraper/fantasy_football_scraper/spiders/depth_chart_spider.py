import scrapy

class DepthChartSpider(scrapy.Spider):
    # identifies the spider
    name="depth_charts"

    def start_requests(self):
        urls = [
            "http://www.seahawks.com/team/depth-chart"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        self.log(response.url.split("/"))

