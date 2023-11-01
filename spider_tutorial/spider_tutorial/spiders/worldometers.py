import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"]

    def parse(self, response):

        countries = response.xpath('//td/a')
        #title = response.xpath('//h1/text()').get()
        #print(countries)
        #print(response.xpath('//td/a/text()').getall())

        for country in countries:
            # . is important to reference the country xpath received from response object
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            # absolute_url = f'https://www.worldometers.info/{link}'
            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url=absolute_url)

            #relative_url
            yield response.follow(url=link, callback=self.parse_country, meta={'country': country_name})

            # {
                #'title':title,
                # 'countries':countries
                # 'country_name': country_name,
                # 'link': link,
            # }

    def parse_country(self, response):
        # response.xpath(('//table[@class="table table-striped table-bordered table-hover table-condensed table-list"]'))
        country = response.request.meta['country']
        rows = response.xpath("(//table[contains(@class, 'table')])[1]/tbody/tr")

        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield {
                'country': country,
                'year': year,
                'population': population,
            }