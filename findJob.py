from selenium import webdriver
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException


class FindJob():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)
        dataframe = pd.DataFrame(
            columns=["Title", "Location", "Company", "Salary", "Description"])
        # self.driver.minimize_window()
        for cnt in range(0, 30, 10):
            self.driver.get(
                "https://www.indeed.com/jobs?q=data+science&l=United+States&start=" + str(cnt))

            sleep(10)

            try:
                pop_up = 'None'

                jobs = self.driver.find_elements_by_class_name('result')

                for job in jobs:
                    result = job.get_attribute('innerHTML')
                    soup = BeautifulSoup(result, 'html.parser')

                    title = soup.find(
                        "a", class_="jobtitle").text.replace('\n', '')
                    location = soup.find(class_="location").text
                    employer = soup.find(
                        class_="company").text.replace('\n', '').strip()
                    try:
                        salary = soup.find(class_="salary").text.replace(
                            '\n', '').strip()
                    except:
                        salary = 'None'

                    print(title, location, employer, salary)

                    summ = job.find_elements_by_class_name("summary")[0]
                    summ.click()
                    sleep(1)
                    try:
                        job_desc = job.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div/div[1]/div/div[3]/div[2]/div[4]/div/p[2]').text
                    except NoSuchElementException:
                        job_desc = 'None'

                    dataframe = dataframe.append(
                        {'Title': title, 'Location': location, 'Employer': employer, 'Description': job_desc}, ignore_index=True)
            except:
                pop_up = self.driver.find_element_by_xpath(
                    '/html/body/div[4]/div[1]/button')
                pop_up.click()
            dataframe.to_csv("jobs.csv", index=False)



f = FindJob()
