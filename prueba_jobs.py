import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# Búsqueda por ID
results = soup.find(id="ResultsContainer")
#print(results.prettify())

# Búsqueda por clase
job_elements = results.find_all("div", class_="card-content")

"""for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element)
    print(company_element)
    print(location_element)
    print()

# Extraer texto de elemento sin espacios
for job_element in job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
"""
# Búsqueda de elementos por clase y contenido de texto
python_jobs = results.find_all(
    "h2", string=lambda text: "python" in text.lower()
)

# Acceder a tados de los padres
# Se quiere acceder al padre del padre
python_job_elements = [
    h2_element.parent.parent.parent for h2_element in python_jobs
]

"""for job_element in python_job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    print(title_element.text.strip())
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()
"""

# Para acceder a los links de las ofertas
for job_element in python_job_elements:
    # -- snip --
    link_url = job_element.find_all("a")[1]["href"]
    print(link_url)