import scrapy

## link = //a[starts-with(@href,"collection") and (parent::h3|parent::h2)]/@href
## titulo = //a[starts-with(@href,"collection") and (parent::h3|parent::h2)]/text()
## titulo dentro = //h1[@class="documentFirstHeading"]/text()
## cuerpo = //div[@class="field-item even"]//p[not(@class)]/text()

class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections'
    ]
    custom_settings= {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_declassified = response.xpath('//a[starts-with(@href,"collection") and (parent::h3|parent::h2)]/@href').getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url':response.urljoin(link)} )

    def parse_link(self,response, **kwargs):
        link = kwargs['url']
        title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
        paragraph = response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').getall()

        yield {
            'url': link,
            'tilte': title,
            'body': paragraph
        }
