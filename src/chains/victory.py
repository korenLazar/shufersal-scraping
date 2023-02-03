from src.chains.engines.matrix import Matrix


class Victory(Matrix):
    pass

    @property
    def scraper(self):
        from il_supermarket_scarper.scrappers_factory import ScraperFactory
        return ScraperFactory.VICTORY