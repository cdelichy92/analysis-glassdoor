# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

#get a list of companies associated with keyword
def GetCompany(keyword):
    #webdriver and access glassdoor
    wd = webdriver.Firefox()
    wd.get("http://www.glassdoor.com/index.htm")

    time.sleep(1)

    #feed keyword
    textbox = wd.find_elements_by_name("sc.keyword")[1]
    textbox.send_keys(keyword)
    textbox.submit()

    #get content and return list of companies
    page_content = wd.page_source
    soup = BeautifulSoup(page_content)
    group = soup.find_all(class_='name openScope link plain')
    wd.quit() #quit driver
    list_of_companies = []
    for result in group:
        list_of_companies.append(result.get_text())
    return list_of_companies


#get reviews associated with 'job' in 'company'
def GetReview(job,company):
    #webdriver and access glassdoor
    wd = webdriver.Firefox()
    wd.get("http://www.glassdoor.com/Reviews/index.htm")

    time.sleep(1)

    #search company
    textbox = wd.find_elements_by_name("sc.keyword")[1]
    textbox.send_keys(company)
    textbox.submit()

    #retrieve page content
    page_content = wd.page_source
    soup = BeautifulSoup(page_content)
    group = soup.find_all('a', {'class': 'eiCell cell reviews'})[0]['href']

    #load address for review
    new_address = "http://www.glassdoor.com" + group + "?filter.jobTitleFTS=" + job + "&filter.defaultEmploymentStatuses=false&filter.employmentStatus=REGULAR&filter.employmentStatus=PART_TIME#trends-overallRating"

    ##code ends here, below is a test, to modify
    #TO DO: connect to glassdoor with user credentials
    #retrieve reviews
    #don't forget to quit driver
    wd.get("http://www.glassdoor.com/Reviews/index.htm")
    page_content = wd.page_source
    soup = BeautifulSoup(page_content)
    return soup

#tests
#print GetCompany('software')
#print GetReview('Software+Engineer','Google')
