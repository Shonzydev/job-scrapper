from dataclasses import dataclass

@dataclass
class Job:
    title : str
    company : str
    url : str
    source : str
    location : str = "Not specified"
    salary : str = "Not specified"
    remote : bool = True


if __name__ == "__main__":
    job = Job(title="Junior python dev",company="microsoft",url="https://ejemplo.com",source="test")

    print(job)