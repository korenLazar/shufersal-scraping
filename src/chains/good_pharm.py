from src.chains.engines.matrix import Matrix
from il_supermarket_scarper.scrappers_factory import ScraperFactory


class GoodPharam(Matrix):
    @property
    def scraper(self):
        return ScraperFactory.GOOD_PHARM
