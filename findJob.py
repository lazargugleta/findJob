from selenium import webdriver
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup


class FindJob():
    def __init__(self):
        self.driver = webdriver.Chrome()
        dataframe = pd.DataFrame(
            columns=["Title", "Location", "Company", "Salary", "Description"])
        # self.driver.minimize_window()
        for cnt in range(0, 50, 10):
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
                    job_desc = self.driver.find_element_by_id('vjs-desc').text

                    dataframe = dataframe.append(
                        {'Title': title, 'Location': location, 'Employer': employer, 'Description': job_desc}, ignore_index=True)
            except:
                pop_up = self.driver.find_element_by_xpath(
                    '/html/body/table[2]/tbody/tr/td/div[2]/div[2]/div[4]/div[3]/div[2]/a')
                pop_up.click()
            dataframe.to_csv("jobs.csv", index=False)



f = FindJob()
