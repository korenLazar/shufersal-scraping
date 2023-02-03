from src.chains.engines.cerberus_web_client import CerberusWebClient


class StopMarket(CerberusWebClient):
    _date_hour_format = "%Y-%m-%d %H:%M:%S"

    @property
    def scraper(self):
        from il_supermarket_scarper.scrappers_factory import ScraperFactory
        return ScraperFactory.STOP_MARKET