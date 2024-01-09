import requests
from bs4 import BeautifulSoup

def main (word_search):
    # Lo primero es obtener el link de la palabra a buscar
    URL = f"https://www.bing.com/search?q={word_search}"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Se coge el contenedor donde se guardan las búsquedas
    results = soup.find(id="b_results")

    # Extraer las URL de los resultados de búsqueda
    url_elements = results.find_all("a", class_="tilk")

    for url_element in url_elements:
        link_url = url_element["href"]
        name_url = url_element.find_all("div", class_="tptt")[0].text.strip()
        print(f"Nombre: {name_url} \t URL: {link_url}")

main("enthec")