from models import Job
def es_internship(x):
    return "intern" in x.lower()

print(es_internship("senior engineer"))
print(es_internship("python intern"))


def contar_remotos(lista):
    count = 0
    for job in lista:
            if job.remote:
                count += 1
            return count

jobs= [
    Job(title="Python intern",company="Anthropic",url="https://ejemplo1.com",source="Devian",remote=True),
    Job(title="Python seenior",company="OpenIA",url="https://ejemplo1.com",source="Inex",remote=True)
]

print(contar_remotos(jobs))