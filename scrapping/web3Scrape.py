import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

class web3Scrape:
    # 생성자 ----------------------------
    def __init__(self, link):
        self.link = link
        self.soup, self.response = self.Scrapping(self.link)
        self.playWr(self.link)
        self.pagingToggle = True
        
        self.jobsID = []
        self.jobs = []
        
        nullCheck = self.soup.find("h1").text
        if(nullCheck == "404"):
            print("null")
            return

        self.scrapePageID()
        
        while(self.pagingToggle):
            newlink = self.paging()
            if(newlink):
                self.playWr(newlink)
                self.scrapePageID()

        self.jobsID = list(set(self.jobsID))

        for i in self.jobsID:
            contentLink = self.link + "/" + i
            print(contentLink)
            self.playWr(contentLink)
            self.scrappingContent()
            print(self.jobs)
        
    def getterJob(self):
        return self.jobs
    
    def playWr(self, pageLink):
        p = sync_playwright().start()
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(pageLink)
        time.sleep(0.001)
        content = page.content()
        p.stop()

        self.soup = BeautifulSoup(content, "html.parser")

    def jobVO(self, title, company, compensation, location):
        job = {
            "title"       : title,
            "company"     : company, 
            "compensation" : compensation,
            "location"     : location,
        }

        return job



    def scrapePageID(self):
        jobid_elements = self.soup.find_all(attrs={'data-jobid': True})

        for element in jobid_elements:
            self.jobsID.append(element['data-jobid'])
            

    def paging(self):
        next_page_links = self.soup.find('a', rel='next')
        if next_page_links:
            newLink = "https://web3.career/" + next_page_links['href']
            return newLink
        else:
            self.pagingToggle = False
            return


    def Scrapping(self, link):
        print(link)
        response = requests.get(link, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        soup = BeautifulSoup(response.content, "html.parser")

        return soup, response
    
    def scrappingContent(self):
        job = self.soup.find('header')
        company   = self.soup.find('div', class_="position-sticky")
        
        if(job and company):
            title = job.find("h1").text
            compensation = job.find("div", class_="mt-4")
            
            if(compensation):
                compensation = compensation.find("p").text
                compensation = compensation.replace('Compensation: ', "")
            else:
                compensation = ""
            

            location     = job.find("div", class_="mt-3")
            
            if(location):
                location = location.find("p").text
                location = location.replace('Location: ', "")
            else:
                location = ""
            
            company      = company.text

            self.jobs.append(self.jobVO(title, company, compensation, location))

        


