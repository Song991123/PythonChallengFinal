from flask import Flask, render_template, request
from scrapping.berlinScrape import berlinScrape
from scrapping.wwrScrape import wwrScrape
from scrapping.web3Scrape import web3Scrape

app = Flask(__name__)


@app.route("/") 
def home():
    return render_template("home.html", name="maren")

@app.route("/search")
def search():
    keyword= request.args.get("keyword")
    
    berlinLink = f"https://berlinstartupjobs.com/skill-areas/{keyword}"
    web3Link   = f"https://web3.career/{keyword}-jobs"
    wwrLink    = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}"

    berlinJobs = berlinScrape(berlinLink).getterJob()
    wwrJobs = wwrScrape(wwrLink).getterJob()
    web3Jobs = web3Scrape(web3Link).getterJob()

    return render_template("search.html", keyword=keyword, berlinJobs=berlinJobs, wwrJobs=wwrJobs, web3Jobs=web3Jobs)
    


if __name__ == "__main__":
    app.run()
