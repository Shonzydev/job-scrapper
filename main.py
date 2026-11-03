import requests
from models import Job


class BaseProvider:
    name = ""
    url = ""
    headers = {}
    items_key = ""

    def fetch(self):
        jobs = []
        response =  requests.get(self.url, headers = self.headers,timeout=10)

        if response.status_code != 200:
            return jobs
        data = response.json()
        for item in data[self.items_key]:
            jobs.append(self.parse(item))
        return jobs

    def parse(self,item):
        raise NotImplementedError

            
class RemotiveProvider(BaseProvider):
    name = "Remotive"
    url = "https://remotive.com/api/remote-jobs"
    items_key =  "jobs"

    def parse(self, item):
        return Job(
            title= item.get("title") or "Not specified",
            company= item.get("company_name") or "Not specified",
            url= item.get("url") or "Not specified",
            source= self.name,  
            location= item.get("candidate_required_location") or "Not specified",
            salary = item.get("salary") or "Not specified",
            remote= True
            )




class TheMuseProvider:
    def __init__(self):
        self.url =  "https://www.themuse.com/api/public/jobs?page=1&level=Internship"
        self.name = "The Muse"

    def fetch(self):
        jobs = []
        response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if response.status_code != 200:
            return jobs
        data = response.json()
        for item in data["results"]:
            names = []
            for loc in item.get("locations") or []:
                names.append(loc.get("name"))
            location = ", ".join(names) or "Not specified"
            job = Job(
                title= item.get("name") or "Not specified",
                company= (item.get("company") or {}).get("name") or "Not specified",
                url= (item.get("refs") or {}).get("landing_page") or "Not specified",
                source= self.name,
                location= location,
                salary= "Not specified",
                remote = False
            )
            jobs.append(job)
        return jobs


if __name__ == "__main__":
    p = RemotiveProvider()
    jobs = p.fetch()
    print(len(jobs))     # entre 10 y 12
    print(jobs[0])
