import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

class wwrScrape:
    # 생성자 ----------------------------
    def __init__(self, link):
        self.link = link
        self.soup, self.response = self.Scrapping(self.link)
        
        self.pages = []
        self.jobs = []

        self.pageToggle = False

        nullCheck = self.soup.find("div", class_="no_results")
        
        if(nullCheck):
            print("null")
            return
        
        self.paging()
        
        self.scrappingContent()

        if (self.pages):
            # 페이지가 존재시
            for page in self.pages:
                pageLink = f"https://weworkremotely.com{page}"
                self.pageToggle = True
                self.playWr(pageLink)
                self.scrappingContent()
            
    def getterJob(self):
        return self.jobs

    def jobVO(self, title, company, position, region):
        job = {
            "title"       : title,
            "company"     : company, 
            "position"    : position,
            "region"      : region,
        }

        return job

    def Scrapping(self, link):
        response = requests.get(link, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        soup = BeautifulSoup(response.content, "html.parser")

        return soup, response

    def playWr(self, pageLink):

        p = sync_playwright().start()
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(pageLink)
        time.sleep(0.001)
        content = page.content()
        p.stop()

        self.soup = BeautifulSoup(content, "html.parser")

    def scrappingContent(self):
        jobList = []
        
        if (self.pageToggle):
            jobList = self.viewAllPageScrape()
        else:
            jobList = self.SingPage()


        for joblist in jobList:
            title = self.get_job(joblist).text
            company, position, region = joblist.find_all("span", class_="company")
            company  = company.text
            position = position.text
            region   = region.text

            self.jobs.append(self.jobVO(title, company, position, region))
            
    def get_job(self, jobList):
        jobs = jobList.find("span", class_="title")
        return jobs
    
    def paging(self):
        viewAll = self.soup.find_all("li", class_="view-all")
        viewAllLenth = len(viewAll)
        
        if(viewAllLenth):
            for i in range(viewAllLenth):
                pageLink = self.soup.find("li", class_="view-all").find("a").attrs['href']
                self.pages.append(pageLink)
                self.soup.find("li", class_="view-all").parent.decompose()
        
    
    def SingPage(self):
        jobPositions = self.soup.find_all("section", class_="jobs")
        jobList = []
        for jobPosition in jobPositions:
            jobList += jobPosition.find_all("li")
        
        return jobList
    
    def viewAllPageScrape(self):
        jobList = self.soup.find("section", class_="jobs").find_all("li")[1:-1]
        return jobList