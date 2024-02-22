import scrapy
class IdealoProductsSpider(scrapy.Spider):
    name = "idealo_products"
    allowed_domains = ["www.idealo.co.uk"]
    start_urls = ["https://www.idealo.co.uk/cat/3751/laptops.html"]
    def parse(self, response):
        # Extract product information from the current page
        products = response.css('div.sr-resultList.resultList--GRID')
        for product in products:
            yield {
                'title': product.css('div.sr-productSummary__title::text').get(),
                'price': product.css('div.sr-detailedPriceInfo__price::text').get(),
                'url': response.urljoin(product.css('h3 a::attr(href)').get())
            }
        # Extract the URL of the next page
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
