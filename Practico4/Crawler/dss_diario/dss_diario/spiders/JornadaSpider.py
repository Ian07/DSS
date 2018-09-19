import scrapy
from dss_diario.items import DssDiarioItem

class JornadaSpider(scrapy.Spider):
    name = "jornada-spider"

    def start_requests(self):
        urls = [
            'http://www.diariojornada.com.ar/provincia/',
            'http://www.diariojornada.com.ar/policiales/',
            'http://www.diariojornada.com.ar/sociedad/',
            'http://www.diariojornada.com.ar/deportes/',
            'http://www.diariojornada.com.ar/paismundo/',
            'http://www.diariojornada.com.ar/economia/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_seccion)

    def parse_noticia(self,response):
        item = DssDiarioItem()
        item['id'] = int(response.url[32:38])
        item['categoria'] = response.xpath('//a[@id="ContentPlaceHolder1_hl_Seccion"]/text()')[0].extract()
        item['titulo'] = response.xpath('//span[@id="ContentPlaceHolder1_lbl_Titulo"]/text()')[0].extract()
        item['copete'] = response.xpath('//span[@id="ContentPlaceHolder1_lbl_Copete"]/text()')[0].extract()
        item['cuerpo'] = "".join([o for o in map(lambda x: x.strip(),response.xpath('//span[@id="ContentPlaceHolder1_lbl_Cuerpo"]/text()').extract())])
        item['hits'] = int(response.xpath('//span[@id="ContentPlaceHolder1_lbl_Hits"]/text()').extract()[0].replace('.',''))
        yield item


    def parse_seccion(self, response):
        noticias_importantes_str = '//div[re:test(@id, "ContentPlaceHolder1_home_bloque_seccion_RP_Bloque_\d_pnl_Titulo_\d$")]//a/@href'
        noticias_secundarias_str = '//a[re:test(@id, "ContentPlaceHolder1_RP_Noticias_hl_Titulo_\d$")]/@href'
        noticias_importantes = response.xpath(noticias_importantes_str)
        noticias_secundarias = response.xpath(noticias_secundarias_str)
        noticias = noticias_importantes + noticias_secundarias
        for href in noticias:
            url = href.extract()
            yield scrapy.Request(url=url, callback = self.parse_noticia)

    
