from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd


class BoxOffice:

    def __init__(self, url):
        """
        Create new Instance of Chrome
        """
        options = webdriver.ChromeOptions()
        options.headless = True
        self.rows = []
        self.headers = []
        self.driver = webdriver.Chrome(
            options=options, executable_path='/path/to/chromedriver')
        self.driver.get(url)

    def next_page(self):
        """
        Jumping to the next page
        """
        try:
            next_page = self.driver.find_element(
                By.XPATH, '//*[@id="a-page"]/main/div/div/div[4]/ul/li[3]/a')
            # Jump to the next page
            next_page.click()
            self.data_scrap()
        except NoSuchElementException:
            print('Data scraping completed')

    def data_scrap(self):
        """
        Scraping data from boxofficemojo site
        """
        html = self.driver.execute_script('return document.body.innerHTML;')
        self.soup = BeautifulSoup(html, 'lxml')

        # extract table from the web
        tables = self.soup.find(
            'div', class_='a-section imdb-scroll-table-inner').find_all('table')

        # Get all of the headers from the table
        if len(self.headers) == 0:
            self.headers = [item.text for item in tables[0].find_all('th')]

        # Get all of the rows from the table
        row_soup = tables[1].find_all('tr')

        self.rows.extend([cell.text for cell in row.findAll('td')]
                         for row in row_soup[1:])

        # Jump to the next page
        self.next_page()

    def create_dataframe(self):
        """
        Create the pandas DataFrame
        """
        self.df = pd.DataFrame(self.rows, columns=self.headers)

    def create_csv_file(self):
        """
        write to csv file
        """
        self.df.to_csv('boxoffice.csv', index=False)

    def close_session(self):
        """
        Here driver.quit function is used to close Chrome driver
        """
        self.driver.quit()


if __name__ == "__main__":
    url = 'https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?area=XWW'

    box_office = BoxOffice(url)

    print('-----------Data Scraping--------------')
    box_office.data_scrap()
    print('-----------Creating Dataframe--------------')
    box_office.create_dataframe()
    print('-----------Creating csv file--------------')
    box_office.create_csv_file()
    print('-----------Closing Webdriver Session--------------')
    box_office.close_session()
    print('-----------Task Completed--------------')
