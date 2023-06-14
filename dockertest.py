import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
import os 


# importing Webdriver Chrome Options from selenium 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# importing webdriver
from selenium import webdriver

# # ...
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

# Setting up the chromium options 
def set_chrome() -> Options:
    # setting up the options for the chromium 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs={}
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-features=InterestCohort')
    chrome_options.experimental_options["prefs"]= chrome_prefs
    chrome_prefs["profile.default_content_settings"]={"images":2}
    return chrome_options

if __name__=="__main__":
        driver =webdriver.Chrome(options=set_chrome())

        email= os.getenv('slack_token')
        password= os.getenv('slack_scraper_token')
        
        data_analyst="https://in.indeed.com/jobs?q=Data+Analyst&l=India&from=searchOnHP&vjk=83e9c11139c0c4e3"

        driver.get(data_analyst)
        # print("Page URL:", driver.current_url) 
        # print("Page Title:", driver.title)

        driver.get(data_analyst)
        sleep(10)

        page_source = driver.page_source
        # print(page_source)

        soup = BeautifulSoup(page_source, 'html.parser')
        #prettified_page = soup.prettify()
        # print(f'Printing the downloaded page', soup)


        # Job_title = soup.find('div',class_="css-1m4cuuf e37uo190")
        # print(Job_title[5].text)

        Job_title = soup.find_all('div',class_="css-1m4cuuf e37uo190")
        # j_t= Job_title[5].text
        # print(len(j_t))

        # print(Job_title[5].text)
        # print(f'printing the title of one of the job',Job_title[2].text)

        def scroll_down():
            # Get the body element and send the PAGE_DOWN key
            body = driver.find_element(By.TAG_NAME,"body")
            body.send_keys(Keys.PAGE_DOWN)

        # function to get the details of all the JOB-titles 
        def get_title(Soup):
            Job_title=soup.find_all('div',class_="css-1m4cuuf e37uo190")
            Job_Heading=[]
            for i in range(0,len(Job_title)):
                name=Job_title[i].text.strip('new')
                Job_Heading.append(name)
            return Job_Heading

        # Organisation name 
        org_name=soup.find_all('div',class_="heading6 company_location tapItem-gutter companyInfo")
        #org_tag=org_name[0].find('span').text
        # print(org_tag)

        # Function to get the organisation Name 
        def get_org_details(Data):
            org_name=soup.find_all('div',class_="heading6 company_location tapItem-gutter companyInfo")
            Company=[]
            for i in range(len(org_name)):
                name=org_name[i].find('span').text
                split=name.strip(".")
                Company.append(split)
            return Company



        # Function to get the JOB-Location 
        def get_location(Data):
            location_tag=soup.find_all('div',class_="companyLocation")
            Loc=[]
            for i in range(len(location_tag)):
                name=location_tag[i].text
                Loc.append(name)
            return Loc


        a_tag= soup.find_all('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')

        def get_job_link(Data):
            a_tag= soup.find_all('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')
            print(a_tag)
            a_tag[0]['href']
            job_li=[]
            for i in range(len(a_tag)):
                l= a_tag[i]['href']
                z="indeed.com"
                y= z+l
                job_li.append(y)
            return job_li



        # # Function to get the Job-Description 

        def get_description(Data):
            job_description= soup.find_all('div',class_="job-snippet")
            Job_des=[]
            for i in range(len(job_description)):
                name=job_description[i].text.strip('\n')
                name1=name.strip('\uf0a7')
                Job_des.append(name1)
            return Job_des


        def details(soup):
            #Details for JOB Heading
            Job_Heading=get_title(soup)
            
            #Details for Company Name     
            Company=get_org_details(soup)
            
            #Getting details for the location of Job-Posting
            Loc=get_location(soup)

            # Getting the details for the Job url 
            Link =get_job_link(soup)
            

            Job_des=get_description(soup)

            # #Getting the details for the date of Job-Posting
            # date=get_dates(Soup)
                
            # # Getting the details for the Salary
            # salary_data=get_Salary(Soup)

            Columns_names=['JOB-Title','Organinsation','Location','Job-Description','Date-of-Posting','Salary']
            Dict_data={
                        'JOB-Title' : Job_Heading,
                        'Organinsation' : Company,
                        'Location' : Loc,
                        #'Ratings' : Ratings,
                        'Job-link' : Link,
                        'Job-Description' :Job_des,
                        #    'Date-of-Posting'  :date,
                        #    'Salary' : salary_data
                    }
            Df=pd.DataFrame(Dict_data)
            
            return Df

        # #List of links for the different Job Roles
        # role_links=[data_analyst,business_analyst,Product_analyst]

        


        D_A = details(soup)
        # Data_Frame=pd.concat(DF_list,ignore_index=True)
        D_A.to_csv("JOBS.CSV",index=None)

        import file_sharing
        file= file_sharing.send_file()
        
