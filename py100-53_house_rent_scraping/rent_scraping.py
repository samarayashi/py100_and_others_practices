import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement
from selenium.common.exceptions import NoSuchElementException

DRIVER_PATH = "./chromedriver.exe"

# agents pools
agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"
]
languages = ["en-US", "en-GB", "en-CA", "en,en_US"]


class HouseCrawler:
    def __init__(self, driver_path: str, random_agent: bool):
        opts = Options()
        if random_agent:
            opts.add_argument(f"user-agent={random.choice(agents)}")
            opts.add_experimental_option('prefs', {'intl.accept_languages': random.choice(languages)})
        self.driver = webdriver.Chrome(executable_path=driver_path, options=opts)
        self.driver.maximize_window()
        self.house_info_list = []

    def deal_with_captcha(self):
        """if bump into captcha, try press check-button 3secs"""
        if self.driver.title == "":
            print("we bump into a captcha")
            hold = self.driver.find_element_by_id('px-captcha')
            webdriver.ActionChains(self.driver).click_and_hold(hold).pause(3).release(hold).perform()
            time.sleep(3)

    def scroll_end(self):
        """scroll down to touch off ajax, let web show all information"""
        search_page = self.driver.find_element_by_css_selector("div#search-page-list-container h1")
        search_page.click()
        for _ in range(10):
            webdriver.ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(0.3)

    def scraping_zillow(self, search_url: str, total_pages: int):
        self.driver.get(search_url)
        time.sleep(3)

        for page_number in range(1, total_pages + 1):
            self.deal_with_captcha()
            self.scroll_end()
            house_items = self.driver.find_elements_by_css_selector("div#grid-search-results li article")

            # capture needed elements in this page
            house: WebElement
            for house in house_items:
                link = house.find_element_by_css_selector("div.list-card-info > a").get_attribute("href")
                if "http" not in link:
                    link = f"https://www.zillow.com{link}"
                address = house.find_element_by_css_selector("div.list-card-info address").text
                price = house.find_element_by_css_selector("div.list-card-price").text
                self.house_info_list.append({"link": link, "address": address, "price": price})

            # try to click next page button
            try:
                next_button = self.driver.find_element_by_css_selector('li>a[rel="next"][title="Next page"]')
                before_url = self.driver.current_url
                next_button.click()
                time.sleep(1)
                if before_url == self.driver.current_url:
                    print(f"It's the last page.({page_number}) ")
                    break
            except NoSuchElementException:
                print(f"only one page")
                time.sleep(100)
                break

    def entry_data(self, form_url: str):
        for house_info in self.house_info_list:
            self.driver.get(form_url)
            time.sleep(0.5)
            columns = self.driver.find_elements_by_css_selector("input.whsOnd.zHQkBf")
            submit = self.driver.find_element_by_css_selector("div[role=button]")
            columns[0].send_keys(house_info["address"])
            columns[1].send_keys(house_info["price"])
            columns[2].send_keys(house_info["link"])
            submit.click()


if __name__ =="__main__":
    crawler = HouseCrawler(DRIVER_PATH, random_agent=True)
    target_page = "https://www.zillow.com/new-rochelle-ny/1-_beds/2_p/?searchQueryState=%7B%22usersSearchTerm%22%3A%22New%20Rochelle%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.05146268457032%2C%22east%22%3A-73.5117593154297%2C%22south%22%3A40.85753084788609%2C%22north%22%3A40.99501202177903%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A26114%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22beds%22%3A%7B%22min%22%3A1%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%2C%22land%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22pagination%22%3A%7B%22currentPage%22%3A2%7D%7D"
    crawler.scraping_zillow(target_page, total_pages=1)
    google_form = "https://docs.google.com/forms/d/e/1FAIpQLSc5b57ETGO8Nfr8YsAX18rgkToEyVqH-dT6DX9LRRU7lr9SMA/viewform?usp=sf_link"
    crawler.entry_data(form_url=google_form)

