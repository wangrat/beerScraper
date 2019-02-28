import re

import scrapy
import scrapy_splash

from beerScraper.items import Beer


# this example needs the scrapyjs package: pip install scrapyjs
# it also needs a splash instance running in your env or on Scrapy Cloud (https://github.com/scrapinghub/splash)
class SplashSpider(scrapy.Spider):
    name = 'splash-spider'

    start_url = 'http://www.ratebeer.com/beer/'

    cookies = {
        'cookie: __cfduid': 'd9821ce6aa0cffa4e50d2f8ab3bbf08811549476420',
        '_ga': 'GA1.2.137750538.1549476422',
        'ASPSESSIONIDAAAQABTR': 'ICLABOEBFLKBBAEBDEAHBNNK',
        '_CookieConsent': 'granted',
        'expiration': '2^%^2F6^%^2F2020+6^%^3A21^%^3A35+PM',
        'idtoken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlFURkNRa1pCUlRnNE4wVXlNMFJET1RNeFF6WXlSakUyTTBORVJVWTJOVVExTlVRMU1qRXdSQSJ9^%^2EeyJuYW1lIjoiQWRhbSBNYXJpYW4gV2FuZ3JhdCIsImVtYWlsIjoiYW12YW5ncmFkdEBnbWFpbC5jb20iLCJnaXZlbl9uYW1lIjoiQWRhbSIsImZhbWlseV9uYW1lIjoiV2FuZ3JhdCIsImdlbmRlciI6Im1hbGUiLCJwaWN0dXJlIjoiaHR0cHM6Ly9wbGF0Zm9ybS1sb29rYXNpZGUuZmJzYnguY29tL3BsYXRmb3JtL3Byb2ZpbGVwaWMvP2FzaWQ9MTY5MDgyODYwNDI4Njc2MSZoZWlnaHQ9NTAmd2lkdGg9NTAmZXh0PTE1NTIwNjkyNzImaGFzaD1BZVJsTnktQ3BnLXluSnBPIiwicGljdHVyZV9sYXJnZSI6Imh0dHBzOi8vcGxhdGZvcm0tbG9va2FzaWRlLmZic2J4LmNvbS9wbGF0Zm9ybS9wcm9maWxlcGljLz9hc2lkPTE2OTA4Mjg2MDQyODY3NjEmd2lkdGg9OTk5OTk5JmV4dD0xNTUyMDY5MjcyJmhhc2g9QWVTWHhmNDRudVBGTUlqbyIsImFnZV9yYW5nZSI6eyJtYXgiOjIwLCJtaW4iOjE4fSwiY29udGV4dCI6eyJtdXR1YWxfbGlrZXMiOnsiZGF0YSI6W10sInN1bW1hcnkiOnsidG90YWxfY291bnQiOjEwMH19LCJpZCI6ImRYTmxjbDlqYjI1MFpBWGgwT2dHUXN0T083S3VpdlJ4UGhVUVc1WkM2cGVuVGN2NElCTUtlQnNPQ3pyOW15MGp3RWVKWkJHcDFSalIyTEdZeFI5WVNLWUxwYjRYNGo5UlpDZ0F6MTVUdFM3dDhKczBTRG1GZ2JRdWcxSDV1RmtrbXBjWkQifSwiY292ZXIiOnsib2Zmc2V0X3giOjUwLCJvZmZzZXRfeSI6NTEsInNvdXJjZSI6Imh0dHBzOi8vcGxhdGZvcm0tbG9va2FzaWRlLmZic2J4LmNvbS9wbGF0Zm9ybS9jb3ZlcnBpYy8^%^5FYXNpZD0xNjkwODI4NjA0Mjg2NzYxJmV4dD0xNTQ4Nzg3Njc0Jmhhc2g9QWVTdXFhOE9iOVpqMkFkOSJ9LCJkZXZpY2VzIjpbeyJvcyI6IkFuZHJvaWQifV0sInVwZGF0ZWRfdGltZSI6IjIwMTgtMTItMjdUMTU6Mzk6MDUrMDAwMCIsImluc3RhbGxlZCI6dHJ1ZSwiaXNfdmVyaWZpZWQiOmZhbHNlLCJsaW5rIjoiaHR0cHM6Ly93d3cuZmFjZWJvb2suY29tL2FwcF9zY29wZWRfdXNlcl9pZC9ZWE5wWkFEcEJXRVpBV2MzQnlNbTlhYjFZM01EbG1Wbmh0YTJ0d2NWTTFObG93Vkd4VlNsUnZiMUZ5VVZkWkFkMFZxVW1oMExUVm9NR1pBQk1rNTVOelpBTFZUWkFNWVZrNFdtNVhibmxwTkZGUGJUbFBUMlJNYURCRlgwcFVNbVZvU1dWWVJWcERUWFpBcVQybHFWVEI1Y0VVemJXbEhjMnhpWkFrRVpELyIsImxvY2FsZSI6InBsX1BMIiwibWlkZGxlX25hbWUiOiJNYXJpYW4iLCJuYW1lX2Zvcm1hdCI6IntmaXJzdH0ge2xhc3R9IiwidGltZXpvbmUiOjEsInRoaXJkX3BhcnR5X2lkIjoiOHVQNHVjb1RDbnRMNzRqVm9qMjZNQ2xyd1VvIiwidmVyaWZpZWQiOnRydWUsIm5pY2tuYW1lIjoiYW12YW5ncmFkdCIsInNob3J0X25hbWUiOiJBZGFtIiwiaW5zdGFsbF90eXBlIjoiVU5LTk9XTiIsInNlY3VyaXR5X3NldHRpbmdzIjp7InNlY3VyZV9icm93c2luZyI6eyJlbmFibGVkIjp0cnVlfX0sInZpZGVvX3VwbG9hZF9saW1pdHMiOnsibGVuZ3RoIjoxNDQ2MCwic2l6ZSI6Mjg2MzMxMTUzMDZ9LCJ2aWV3ZXJfY2FuX3NlbmRfZ2lmdCI6ZmFsc2UsInVzZXJfbWV0YWRhdGEiOnt9LCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiY2xpZW50SUQiOiJ2eTN2UXhLRlh2TXlYVGpkZGtNaURKQVVGdWNiOHZkdSIsInVwZGF0ZWRfYXQiOiIyMDE5LTAyLTA2VDE4OjIxOjEyLjQ5NloiLCJ1c2VyX2lkIjoiZmFjZWJvb2t8MTY5MDgyODYwNDI4Njc2MSIsImlkZW50aXRpZXMiOlt7InByb3ZpZGVyIjoiZmFjZWJvb2siLCJ1c2VyX2lkIjoiMTY5MDgyODYwNDI4Njc2MSIsImNvbm5lY3Rpb24iOiJmYWNlYm9vayIsImlzU29jaWFsIjp0cnVlfV0sImNyZWF0ZWRfYXQiOiIyMDE4LTA1LTI0VDEzOjI4OjI5Ljc5NFoiLCJpc3MiOiJodHRwczovL3JhdGViZWVyLmF1dGgwLmNvbS8iLCJzdWIiOiJmYWNlYm9va3wxNjkwODI4NjA0Mjg2NzYxIiwiYXVkIjoidnkzdlF4S0ZYdk15WFRqZGRrTWlESkFVRnVjYjh2ZHUiLCJpYXQiOjE1NDk0NzcyOTUsImV4cCI6MTU1ODExNzI5NX0^%^2EcHJ9aBEBI7BPv8hB^%^5Fn^%^5FALAEqpGYV8Nyu7r5NvsSiC8ZhV8FNnX5HcxA9Km5xh3ypkU^%^2DjcQG2qOjPFsrTDi7X61g9z1qp1elbvwoXkUvVE9eUkiAKwfzkDJxq3lOux8MWdDXrYLeff2dGJ4CZ1l5Jcyj^%^2Dldo1QksejTzIH30aeRmByjPPZtmjCg^%^2DYv4w1eIA2Bfpa5^%^2DNSqkXei1Hg4Ztx63cJa5djVwNaza8LWSJ5At^%^2DRWe^%^2Dqz5YOKGVgF4lo^%^5FNzw2nfhuOhdSoJ5qsblJVUeHDZsZCvGI^%^2DK^%^5FphJjgO9ti4K3kwlGQidCmphqbWKRKhF6JZKsG8G46vwH7BlAmcOL9Q',
        'SessionID': '10300907',
        'token': 'XIncTtP04ozKNamGx9QXKdpeiSwd07kE',
        'SessionCode': '^%^7B1AE71A16^%^2D92B2^%^2D4E6A^%^2D961B^%^2D666E39E0E588^%^7D',
        'session': 'eyJ1c2VybmFtZSI6IkxhZ2VyVGFwcGVyMTAiLCJpc1ByZW1pdW1NZW1iZXIiOmZhbHNlLCJzZWN1cml0eUxldmVsSWQiOjAsInVzZXJJZCI6IjU2MTIwMiIsImltYWdlVXJsIjoiaHR0cHM6Ly9yZXMuY2xvdWRpbmFyeS5jb20vcmF0ZWJlZXIvaW1hZ2UvdXBsb2FkL3dfNDAsaF80MCxjX2ZpbGwsZF91c2VyZGVmYXVsdF9kdGdrbGwucG5nLGZfYXV0by91c2VyX0xhZ2VyVGFwcGVyMTAifQ==',
        '_ShareTutorial': 'shown',
        '__atuvc': '4^%^7C6',
        'ASPSESSIONIDAADRBASQ': 'LOLFJBOCIPMCCNOKOMDHBBFF',
        'ASPSESSIONIDAADSAATQ': 'ELFNDJHAHOPIOHBKINFFANAL',
        '__utma': '56588200.137750538.1549476422.1550428816.1550428816.1',
        '__utmc': '56588200',
        '__utmz': '56588200.1550428816.1.1.utmcsr=(direct)^|utmccn=(direct)^|utmcmd=(none)',
        'ASPSESSIONIDACDSDDRQ': 'GLDKPABCLDODNINEGBKENCLI',
        '_gid': 'GA1.2.1462830288.1550930341',
        'ASPSESSIONIDAACTCCQQ': 'DMHAMEHAHKPFKOCDNMPKJEKB',
        '_gaexp': 'GAX1.2.0DrnAWcPQc2kEPXfBbwTcA.18040.1',
        'ASPSESSIONIDAABQCBSR': 'EECKJAEBEMJAKGECGKMOAEAP',
        '_gat': '1',
    }

    headers = {
        'authority': 'www.ratebeer.com',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'referer': 'https://www.ratebeer.com/beer/st-bernardus-christmas-ale/65814/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,pl;q=0.8',
        'if-modified-since': 'Mon, 25 Feb 2019 22:35:14 GMT',
        'Referer': 'https://www.ratebeer.com/beer/st-bernardus-christmas-ale/65814/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Access-Control-Request-Method': 'POST',
        'Origin': 'https://googleads.g.doubleclick.net',
        'Access-Control-Request-Headers': 'authorization,content-type,locale',
        'Upgrade-Insecure-Requests': '1',
        'locale': 'en',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlFURkNRa1pCUlRnNE4wVXlNMFJET1RNeFF6WXlSakUyTTBORVJVWTJOVVExTlVRMU1qRXdSQSJ9.eyJuYW1lIjoiQWRhbSBNYXJpYW4gV2FuZ3JhdCIsImVtYWlsIjoiYW12YW5ncmFkdEBnbWFpbC5jb20iLCJnaXZlbl9uYW1lIjoiQWRhbSIsImZhbWlseV9uYW1lIjoiV2FuZ3JhdCIsImdlbmRlciI6Im1hbGUiLCJwaWN0dXJlIjoiaHR0cHM6Ly9wbGF0Zm9ybS1sb29rYXNpZGUuZmJzYnguY29tL3BsYXRmb3JtL3Byb2ZpbGVwaWMvP2FzaWQ9MTY5MDgyODYwNDI4Njc2MSZoZWlnaHQ9NTAmd2lkdGg9NTAmZXh0PTE1NTIwNjkyNzImaGFzaD1BZVJsTnktQ3BnLXluSnBPIiwicGljdHVyZV9sYXJnZSI6Imh0dHBzOi8vcGxhdGZvcm0tbG9va2FzaWRlLmZic2J4LmNvbS9wbGF0Zm9ybS9wcm9maWxlcGljLz9hc2lkPTE2OTA4Mjg2MDQyODY3NjEmd2lkdGg9OTk5OTk5JmV4dD0xNTUyMDY5MjcyJmhhc2g9QWVTWHhmNDRudVBGTUlqbyIsImFnZV9yYW5nZSI6eyJtYXgiOjIwLCJtaW4iOjE4fSwiY29udGV4dCI6eyJtdXR1YWxfbGlrZXMiOnsiZGF0YSI6W10sInN1bW1hcnkiOnsidG90YWxfY291bnQiOjEwMH19LCJpZCI6ImRYTmxjbDlqYjI1MFpBWGgwT2dHUXN0T083S3VpdlJ4UGhVUVc1WkM2cGVuVGN2NElCTUtlQnNPQ3pyOW15MGp3RWVKWkJHcDFSalIyTEdZeFI5WVNLWUxwYjRYNGo5UlpDZ0F6MTVUdFM3dDhKczBTRG1GZ2JRdWcxSDV1RmtrbXBjWkQifSwiY292ZXIiOnsib2Zmc2V0X3giOjUwLCJvZmZzZXRfeSI6NTEsInNvdXJjZSI6Imh0dHBzOi8vcGxhdGZvcm0tbG9va2FzaWRlLmZic2J4LmNvbS9wbGF0Zm9ybS9jb3ZlcnBpYy8_YXNpZD0xNjkwODI4NjA0Mjg2NzYxJmV4dD0xNTQ4Nzg3Njc0Jmhhc2g9QWVTdXFhOE9iOVpqMkFkOSJ9LCJkZXZpY2VzIjpbeyJvcyI6IkFuZHJvaWQifV0sInVwZGF0ZWRfdGltZSI6IjIwMTgtMTItMjdUMTU6Mzk6MDUrMDAwMCIsImluc3RhbGxlZCI6dHJ1ZSwiaXNfdmVyaWZpZWQiOmZhbHNlLCJsaW5rIjoiaHR0cHM6Ly93d3cuZmFjZWJvb2suY29tL2FwcF9zY29wZWRfdXNlcl9pZC9ZWE5wWkFEcEJXRVpBV2MzQnlNbTlhYjFZM01EbG1Wbmh0YTJ0d2NWTTFObG93Vkd4VlNsUnZiMUZ5VVZkWkFkMFZxVW1oMExUVm9NR1pBQk1rNTVOelpBTFZUWkFNWVZrNFdtNVhibmxwTkZGUGJUbFBUMlJNYURCRlgwcFVNbVZvU1dWWVJWcERUWFpBcVQybHFWVEI1Y0VVemJXbEhjMnhpWkFrRVpELyIsImxvY2FsZSI6InBsX1BMIiwibWlkZGxlX25hbWUiOiJNYXJpYW4iLCJuYW1lX2Zvcm1hdCI6IntmaXJzdH0ge2xhc3R9IiwidGltZXpvbmUiOjEsInRoaXJkX3BhcnR5X2lkIjoiOHVQNHVjb1RDbnRMNzRqVm9qMjZNQ2xyd1VvIiwidmVyaWZpZWQiOnRydWUsIm5pY2tuYW1lIjoiYW12YW5ncmFkdCIsInNob3J0X25hbWUiOiJBZGFtIiwiaW5zdGFsbF90eXBlIjoiVU5LTk9XTiIsInNlY3VyaXR5X3NldHRpbmdzIjp7InNlY3VyZV9icm93c2luZyI6eyJlbmFibGVkIjp0cnVlfX0sInZpZGVvX3VwbG9hZF9saW1pdHMiOnsibGVuZ3RoIjoxNDQ2MCwic2l6ZSI6Mjg2MzMxMTUzMDZ9LCJ2aWV3ZXJfY2FuX3NlbmRfZ2lmdCI6ZmFsc2UsInVzZXJfbWV0YWRhdGEiOnt9LCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiY2xpZW50SUQiOiJ2eTN2UXhLRlh2TXlYVGpkZGtNaURKQVVGdWNiOHZkdSIsInVwZGF0ZWRfYXQiOiIyMDE5LTAyLTA2VDE4OjIxOjEyLjQ5NloiLCJ1c2VyX2lkIjoiZmFjZWJvb2t8MTY5MDgyODYwNDI4Njc2MSIsImlkZW50aXRpZXMiOlt7InByb3ZpZGVyIjoiZmFjZWJvb2siLCJ1c2VyX2lkIjoiMTY5MDgyODYwNDI4Njc2MSIsImNvbm5lY3Rpb24iOiJmYWNlYm9vayIsImlzU29jaWFsIjp0cnVlfV0sImNyZWF0ZWRfYXQiOiIyMDE4LTA1LTI0VDEzOjI4OjI5Ljc5NFoiLCJpc3MiOiJodHRwczovL3JhdGViZWVyLmF1dGgwLmNvbS8iLCJzdWIiOiJmYWNlYm9va3wxNjkwODI4NjA0Mjg2NzYxIiwiYXVkIjoidnkzdlF4S0ZYdk15WFRqZGRrTWlESkFVRnVjYjh2ZHUiLCJpYXQiOjE1NDk0NzcyOTUsImV4cCI6MTU1ODExNzI5NX0.cHJ9aBEBI7BPv8hB_n_ALAEqpGYV8Nyu7r5NvsSiC8ZhV8FNnX5HcxA9Km5xh3ypkU-jcQG2qOjPFsrTDi7X61g9z1qp1elbvwoXkUvVE9eUkiAKwfzkDJxq3lOux8MWdDXrYLeff2dGJ4CZ1l5Jcyj-ldo1QksejTzIH30aeRmByjPPZtmjCg-Yv4w1eIA2Bfpa5-NSqkXei1Hg4Ztx63cJa5djVwNaza8LWSJ5At-RWe-qz5YOKGVgF4lo_Nzw2nfhuOhdSoJ5qsblJVUeHDZsZCvGI-K_phJjgO9ti4K3kwlGQidCmphqbWKRKhF6JZKsG8G46vwH7BlAmcOL9Q',
        'content-type': 'application/json',
        'x-client-data': 'CKe1yQEIl7bJAQijtskBCMS2yQEIqZ3KAQioo8oBCLGnygEIv6fKAQjiqMoBGPmlygE=',
        'cookie': '_fbp=fb.1.1550422345019.49096300; __gfp_64b=lGZmLuyB1Q0U6ZkOokxy3V1neDJGokoI9QxTCabK67f.j7; DSID=ADyxukuaImyrRLMpym_h_ezEAu9FsSzQR8adb777w99PLe7Pv_QDaZud3YdPmWhdg6KVVLj-yemE5V34sAI_YozSeY6YwCYYFlspXl7_9ywxdAVSCae8u9U; IDE=AHWqTUnv2lHkKE52vYpK-f7DidWjSL6nGJ176NjYNh74Aid2LLn4t_gmCZ6jveWI',
        'pragma': 'no-cache',
    }

    lua_script = """
    
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(3))
        
        local result, error = splash:wait_for_resume([[
        
            function main(splash) {
                while(document.getElementById("beerName") == null) {
                    setTimeout(function(){}, 2000);
                }
    
    			while(document.getElementById("beerName").innerHTML == undefined || document.getElementById("beerName").innerHTML == "Loading...") {
                    setTimeout(function(){}, 2000);
                }
            
            splash.resume();
            }
        ]])
    
        return {
            html = splash:html()
        }
    end

    """

    def start_requests(self):
        for id in range(11, 100):
            yield scrapy_splash.SplashRequest(self.start_url + str(id) + '/', self.parse,
                                              args={
                                                  'lua_source': self.lua_script
                                              },
                                              meta={'id': id}
                                              )

    def parse(self, response):
        item = Beer()

        item['name'] = str(response.xpath("//h1[@id='beerName']/text()").get())

        item['image_urls'] = [str(response.css("#toggleImage > img::attr(src)").get())]

        item['id'] = response.meta['id']

        if(item['name'] != 'Loading...'):
            yield item
