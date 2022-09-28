from navigator.GSNFTNavigator import MetaBoyNavigator
import traceback

DESIRED_TEXT = "Cosmos"

# Works with navigators that allow iterating through results pages with items in each page that are loaded and extracted
def performRoutine(scraper):
    while True:
        while (item := scraper.nextItem()):
            scraper.extractItem(item)
        scraper.nextPage()

def skipPages(scraper, n):
    for _ in range(n):
        scraper.nextPage()

if __name__ == "__main__":
    scraper = None
    try:
        scraper = MetaBoyNavigator(DESIRED_TEXT)       # Implemented Navigator instantiated here
        performRoutine(scraper)
    except Exception as e:
        traceback.print_exc()
    finally:
        if scraper:
            scraper.cleanUp()


