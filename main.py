
# coding: utf-8

# # Import statments

# In[1]:

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import urllib2
import json

KEYWORD = 'Restaurants'
NBPAGE = 41


# In[2]:

# Data from API call
partnerid = '47233'
key = 'eUgciFSjE5A'
ip='128.12.244.5'
hdr = {'User-Agent': 'Mozilla/5.0'}

partnerid = '47697'
key = 'fM8L4EuhVjC'
ip='128.12.244.5'
hdr = {'User-Agent': 'Mozilla/5.0'}


# # Task: List companies corresponding to a key word

# Using Scrapping

# In[3]:

def GetCompaniesScrapping(keyword,maxLoop):
    
    #Webdriver and access glassdoor
    wd = webdriver.Firefox()
    wd.implicitly_wait(30)
    wd.get("http://www.glassdoor.com/Reviews/index.htm")

    time.sleep(1)

    #Feed keyword
    textbox = wd.find_elements_by_name("sc.keyword")[0]
    textbox.send_keys(keyword)
    textbox.submit()

    list_of_companies = []

    time.sleep(1)

    page_url = wd.current_url[:-3]

    page_number = 0
    earlyStop= False

    while page_number<maxLoop and not earlyStop:

        #get content and return list of companies
        group = wd.find_elements_by_class_name('tightAll')

        if len(group)==0:
            earlyStop = True

        for result in group:
            if "Reviews" not in result.text and result.text!="":
                list_of_companies.append(result.text)
            else:
                pass

        page_number = page_number +1
        wd.get(page_url+"_IP"+str(page_number)+".htm")
        time.sleep(1)

    wd.quit() #quit driver
    return list_of_companies


# In[ ]:




# Using API

# In[4]:

def getCompaniesAPI(keyword,nb_max_pages_results):
    
    from BeautifulSoup import BeautifulSoup

    partnerid = '47233'
    key = 'eUgciFSjE5A'
    ip='128.12.244.5'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    
    query=keyword
    page=1
    urlbase='http://api.glassdoor.com/api/api.htm?t.p='+partnerid+'&t.k='+key+'&userip='+ip+'&useragent=Mozilla/5.0&format=json&v=1&action=employers&q='+query+'&pn='+str(page)

    req = urllib2.Request(urlbase,headers=hdr)
    response = urllib2.urlopen(req)

    soup = BeautifulSoup(response)
    soupjson = json.loads(unicode(soup))

    total_number_of_pages = soupjson['response']['totalNumberOfPages']

    if total_number_of_pages<nb_max_pages_results:
        total_number_of_pages = total_number_of_pages
    else:
        total_number_of_pages=nb_max_pages_results

    list_of_companies = []

    for i in range(total_number_of_pages):

        page = i+1
        urlbase='http://api.glassdoor.com/api/api.htm?t.p='+partnerid+'&t.k='+key+'&userip='+ip+'&useragent=Mozilla/5.0&format=json&v=1&action=employers&q='+query+'&pn='+str(page)

        req = urllib2.Request(urlbase,headers=hdr)
        response = urllib2.urlopen(req)

        soup = BeautifulSoup(response)
        soupjson = json.loads(unicode(soup))

        try:
            list_of_results = soupjson['response']['employers']
            for result in list_of_results:
                name = result['name']
                list_of_companies.append(name)
        except:
            pass

    return list_of_companies


# In[5]:

list_of_companies = getCompaniesAPI(KEYWORD,NBPAGE)
print list_of_companies


# # Task: Reviews

# Using Scrapping

# In[6]:

def GetReviewScrapping(job,company):
    
    wd = webdriver.Firefox()
    wd.implicitly_wait(30)
    wd.get("http://www.glassdoor.com/Reviews/index.htm")

    #search company
    textbox = wd.find_elements_by_name("sc.keyword")[1]
    textbox.send_keys(company)
    textbox.submit()

    link = wd.find_elements_by_class_name('eiCell')[0].get_attribute('href')

    new_address = link + "?filter.jobTitleFTS=" + job + "&filter.defaultEmploymentStatuses=false&filter.employmentStatus=REGULAR&filter.employmentStatus=PART_TIME#trends-overallRating"

    result = []

    try:

        wd.get(new_address)

        wait = WebDriverWait(wd, 30)
        element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "categoryRating")))

        rating = wd.find_elements_by_class_name('ratingNum') 
        
        element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "employerStats")))

        soup = BeautifulSoup(wd.find_elements_by_class_name('employerStats')[0].get_attribute('innerHTML'))
        nb_reviews =soup.find_all('span')[1].text
        
        result = [company,job,nb_reviews,rating[0].text,rating[1].text,rating[2].text,rating[3].text,rating[4].text,rating[5].text]

    except:
        pass
    
    wd.quit()
    
    return result


# In[ ]:




# In[ ]:

def GetListOfReviewsScrapping(list_of_companies,job):
    print "Company" + "\t" + "Job" + "\t" + "Number of reviews" + "\t" + "Overall" + "\t"+ "Culture & Values" + "\t"+ "Work/Life Balance" + "\t"+ "Senior Management" + "\t"+ "Comp & Benefits" + "\t"+ "Career Opportunities" + "\n"
    for company in list_of_companies:
        result =  GetReviewScrapping(job,company)
        print result[0] + "\t" + result[1] + "\t" + result[2] + "\t" + result[3] + "\t" + result[4] + "\t" + result[5] + "\t"+result[6] + "\t" + result[7] + "\t" + result[8] 


# In[ ]:




# Using API

# In[7]:

def GetCompanyRatingAPI(query):
    
    from BeautifulSoup import BeautifulSoup

    partnerid = '47233'
    key = 'eUgciFSjE5A'
    ip='128.12.244.5'
    hdr = {'User-Agent': 'Mozilla/5.0'}

    try:

        page=1
        urlbase='http://api.glassdoor.com/api/api.htm?t.p='+partnerid+'&t.k='+key+'&userip='+ip+'&useragent=Mozilla/5.0&format=json&v=1&action=employers&q='+query+'&pn='+str(page)
        req = urllib2.Request(urlbase,headers=hdr)
        response = urllib2.urlopen(req)
        
        soup = BeautifulSoup(response)
        soupjson = json.loads(unicode(soup))

        result = soupjson['response']['employers'][0]
        try:
            name = result['name']
        except:
            name = query
        job = 'Overall'

        industry = ''
        sector = ''
        try:
            industry = result['industryName']
            sector = result['sectorName']
        except:
            pass

        nb_ratings = ''
        try:
            nb_ratings = str(result['numberOfRatings'])
        except:
            pass

        overall_rating = ''
        culture_and_values = ''
        work_life_balance = ''
        senior_leadership = '' 
        compensation_and_benefits =''   
        career_opportunities =''
        try:
            overall_rating = str(result['overallRating'])
            culture_and_values = str(result['cultureAndValuesRating'])
            work_life_balance = str(result['workLifeBalanceRating'])
            senior_leadership = str(result['seniorLeadershipRating'] )  
            compensation_and_benefits = str(result['compensationAndBenefitsRating']   )    
            career_opportunities = str(result['careerOpportunitiesRating'] ) 
        except:
            pass        

        recommend_to_friend = ''
        name_CEO = ''
        pourcentage_approve_CEO = ''
        try:  
            recommend_to_friend = str(result['recommendToFriendRating']  )
            name_CEO = result['ceo']['name']
            pourcentage_approve_CEO = str(result['ceo']['pctApprove'])
        except:
            pass  

        return  industry + '\t'+sector + '\t'+nb_ratings + '\t'+overall_rating + '\t'+culture_and_values + '\t'+work_life_balance + '\t'+senior_leadership + '\t'+compensation_and_benefits + '\t'+career_opportunities + '\t'+recommend_to_friend + '\t'+name_CEO +'\t'+pourcentage_approve_CEO
    except:
        return ''


def GetRatingsAPI(companies):

    print 'Name' + '\t'+ 'Job' + '\t'+'Industry' + '\t'+'Sector' + '\t'+'Number of ratings' + '\t'+'Overall rating' + '\t'+'Culture and values' + '\t'+'Work life balance' + '\t'+'Senior Leadership' + '\t'+'Compensation and benefits' + '\t'+'Career opportunities' + '\t'+'Recommend to friend' + '\t'+'Name CEO' +'\t'+'Pourcentage approve CEO'
    
    for company in companies:
        try:
            print company + '\t'+ 'Overall' + '\t' + GetCompanyRatingAPI(company.replace (" ", "+"))
        except:
            pass


GetRatingsAPI(list_of_companies)



