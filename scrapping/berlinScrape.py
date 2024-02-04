import requests
from bs4 import BeautifulSoup

class berlinScrape:
    # 생성자 ----------------------------
    def __init__(self, link):
        self.link = link
        self.soup, self.response = self.Scrapping(self.link)
        self.jobs = []
        nullCheck = self.soup.find("body", class_="error404")
        if(nullCheck):
            print("null")
            return
        
        self.page = self.paging(self.soup)
        if self.page > 1:
            for i in range(1, self.page + 1):
                print(f"<page : {i}>")
                print("====================================")
                newLink = f"{self.link}page/{i}"
                self.soup, self.response = self.Scrapping(newLink)
                self.scrappingContent()
        else:
            self.scrappingContent()
    
    def getterJob(self):
        return self.jobs
    
    def jobVO(self, job, company, description, jobLink):
        job = {
            "job"         : job,
            "company"     : company, 
            "description" : description,
            "joblink"     : jobLink,
        }

        return job

    def Scrapping(self, link):
        response = requests.get(link, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        soup = BeautifulSoup(response.content, "html.parser")

        return soup, response

    def scrappingContent(self):
        jobList = self.soup.find_all("li", class_="bjs-jlid")

        for joblist in jobList:
            company = self.get_companys(joblist)
            job = self.get_job(joblist)
            description = self.get_descriptions(joblist)
            jobLink = self.get_jobLinks(joblist)

            self.jobs.append(self.jobVO(job.text, company.text, description.text.strip(), jobLink))
            

    def get_companys(self, jobList):
        companys = jobList.find("a", class_="bjs-jlid__b")
        return companys

    def get_job(self, jobList):
        jobs = jobList.find("h4", class_="bjs-jlid__h")
        return jobs

    def get_descriptions(self, jobList):
        descriptions = jobList.find("div", class_="bjs-jlid__description")
        return descriptions

    def get_jobLinks(self, jobList):
        jobLinks = jobList.find(
            "h4", class_="bjs-jlid__h").find("a").attrs["href"]
        return jobLinks

    def paging(self, soup):
        page = soup.find("ul", class_="bsj-nav").find_all("a")
        if not page:
            return 0
        else:
            return int(page[-2].text)

