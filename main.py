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




class TheMuseProvider(BaseProvider):
    name = "TheMuse"
    url = "https://www.themuse.com/api/public/jobs?page=1&level=Internship"
    headers = {"User-Agent": "Mozilla/5.0"}
    items_key =  "results"

    def parse(self,item):
        names = []
        for loc in item.get("locations") or []:
            names.append(loc.get("name"))
        return Job(
            title= item.get("name") or "Not specified",
            company= (item.get("company") or {}).get("name") or "Not specified",
            url= (item.get("refs") or {}).get("landing_page") or "Not specified",
            source= self.name,
            location = ", ".join(names) or "Not specified",
            salary= "Not specified",
            remote = False)

if __name__ == "__main__":
    providers = [RemotiveProvider(), TheMuseProvider()]
    all_jobs = []
    for provider in providers:
        found = provider.fetch()
        print(provider.name, len(found))
        all_jobs += found
    print(len(all_jobs))


