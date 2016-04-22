# -*- coding: utf-8 -*-
import urllib2
import json
import time
from BeautifulSoup import BeautifulSoup

# Data from API call
partnerid = #ENTER API ID here
key = #ENTER API key here
ip = #ENTER your ip
hdr = #ENTER user agent
urlbase='http://api.glassdoor.com/api/api.htm?t.p='+partnerid+'&t.k='+key+'&userip='+ip+'&useragent='+hdr+'&format=json&v=1&action=jobs-prog&countryId=1&jobTitle='


# Returns result of API call 
def api_call (url):
    
    try:

        req = urllib2.Request(url,headers=hdr)
        response = urllib2.urlopen(req)
            
        soup = BeautifulSoup(response)
        soupjson = json.loads(unicode(soup))

        results = soupjson['response']['results']
        results = sorted(results, key = lambda result: result['frequencyPercent'], reverse = True)
        return results, soupjson['response']
    
    except:
        print "Failure"
        print "url: " + url
        time.sleep(15)
        return api_call(url)

# Write all jobs from "start" job
def jobs_from_start(start):

    # To keep track of what job we need to see
    queue = start
    
    # To keep track of what job we have already seen
    jobidH = {}
    
    # Where we save our results
    fedges = open('job-edges2.csv', 'w')
    fjobs = open('jobs-ids2.csv', 'w')
    
    # Simple counter: how many API calls we made
    i = 0
        
    while queue:

        job_title = queue.pop(0)

        print i

        url = urlbase + job_title.encode('utf-8').replace(' ','+')  
        results = api_call(url)[0]
        response = api_call(url)[1]
        
        # Set that we have seen this job
        jobidH.setdefault(job_title, i)
        
        try:    
            fjobs.write("%s,%d,%s,%s,%s\n" %(job_title.encode('utf-8'), i, response['payLow'], response['payMedian'], response['payHigh']))
        except:
            i += 1
            continue

        for result in results:
            
            #if ((float(result['frequencyPercent']) < 3.5 and int(result['frequency']) < 200) or int(result['nationalJobCount']) < 5000):
            #    continue
            
            result['nextJobTitle'] = result['nextJobTitle'].strip()
            result['nextJobTitle'] = ''.join([c for c in result['nextJobTitle'] if c.islower() or c.isupper() or c==' ']).lower()
            
            try:
                # If next job not already visited, we add that to our list of jobs to visit
                if not (result['nextJobTitle'] in jobidH or result['nextJobTitle'] in queue):
                    queue.append(result['nextJobTitle'])
            
                # Output our edge
                fedges.write("%s,%s,%d,%f,%d\n" %(job_title.encode('utf-8'),result['nextJobTitle'].encode('utf-8'),result['frequency'],result['frequencyPercent'],result['nationalJobCount']))
                
            except:
                continue
            
        i += 1
        time.sleep(0.5)
            
    fedges.close()
    fjobs.close()
    

if __name__ == "__main__":
    
    starting_queue = ['software engineer',
                      'engineer', 
                      'surgeon', 
                      'dentist',
                      'doctor', 
                      'physician', 
                      'lawyer', 
                      'architect', 
                      'assistant professor', 
                      'artist', 
                      'geologist', 
                      'recruiter',
                      'legal intern',
                      'public relations intern']
    jobs_from_start(starting_queue)