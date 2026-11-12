import requests
from models import Job

class BaseProvider:
    pages = 1
    name = ""
    url = ""
    headers = {}
    items_key = ""

    def fetch(self):
        jobs = []
        for page in range(1, self.pages + 1):
            page_url = self.url.format(page=page)
            try : 
                response =  requests.get(page_url, headers = self.headers,timeout=10)
            except requests.exceptions.RequestException as e:
                print(f"Error in {self.name} - {page}", e)
                break
            if response.status_code != 200:
                print(response.status_code)
                break
            try:
                data = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error in {self.name}",e)
                break
            try:
                items = data[self.items_key]
            except KeyError as e:
                print(f"Error in {self.name}: key doesnt exist {e}")
                break

            for item in items:
                try:
                    jobs.append(self.parse(item))
                except  (KeyError, TypeError, AttributeError, ValueError) as e:
                    print(f"Error in {self.name}: item ommited ({type(e).__name__}: {e})")
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
    url = "https://www.themuse.com/api/public/jobs?page={page}&level=Internship"
    headers = {"User-Agent": "Mozilla/5.0"}
    items_key =  "results"
    pages = 3

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


class ArbeitnowProvider(BaseProvider):
    name = "Arbeitnow" 
    url = "https://www.arbeitnow.com/api/job-board-api?page={page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    items_key = "data"
    pages = 2

    def parse(self,item):
        return Job(
            title= item.get("title") or "Not specified",
            company= item.get("company_name") or "Not specified",
            url= item.get("url") or "Not specified",
            source= self.name,
            location= item.get("location"),
            remote= item.get("remote", False)

        )


def filter_jobs(jobs,keywords):
    result = []
    for job in jobs:
        # print(repr(keyword), "|", repr(job.title)) (method code depurations)
        if any(kw.lower() in job.title.lower() for kw in keywords):
            result.append(job)
    return result

if __name__ == "__main__":
    
    providers = [RemotiveProvider(), TheMuseProvider(), ArbeitnowProvider()]

    all_jobs = []
    
    for provider in providers:
        try:
            all_jobs += provider.fetch()
        except Exception as e:
            print(f"error in {provider.name}",type(e).__name__)
            

    resultado =  filter_jobs(all_jobs, ["intern","trainee"])

    print(f"Total: {len(all_jobs)} | Coinciden: {len(resultado)}")

    if resultado:
        for job in resultado:
            print(f"{job.title} | {job.company} | {job.location}")
    else:
        print("Sin resultados")
