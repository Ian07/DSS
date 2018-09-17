import scrapy

class JornadaSpider(scrapy.Spider):
    name = "lucas"

    def start_requests(self):
        urls = [
            'http://www.diariojornada.com.ar/219666/deportes/river_quiere_avanzar_en_la_copa_argentina_frente_a_platense/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'jornada-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
