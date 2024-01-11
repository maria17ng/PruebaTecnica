import requests
from bs4 import BeautifulSoup
import json
# Para que me deje navegar por las hojas y no me blooque
import time
import random

class Scrapper_bing:

    def __init__ (self, word_search, filetype, pages):
        self.URL = "https://www.bing.com/search?q={}&first={}"
        self.word_search = word_search
        self.filetype = filetype
        self.pages = pages
        self.list_pages = []

        self.user_agent = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        ]    
           

    def define_pages (self):
        # Existen tres formatos diferentes: cuando se quiere sólo una hoja "1";
        # cuando se quiere un rango "1:3"; o cuando se quieren todas que es ""

        # Destacar que si quiere la hoja 1, para buscarla es como la 0, si quiere la hoja
        # 2, para buscarla es la 10, la 3 es la 20; y así
        # Por eso se guardan el valor - 1 de lo que se intriduzca

        # Si quiere todas las hojas, y en este caso la lista se queda vacía

        if ":" in self.pages:
            # Es un rango
            inicio, fin = map(int, self.pages.split(":"))
            self.list_pages = list(range(inicio - 1, fin))
            
        elif len(self.pages) != 0:
            # Es un número único
            self.list_pages = [int(self.pages) - 1]
            
        print(self.list_pages)


    def load_results(self, indx_page):
        # Se cargan los resultados de la página indicada

        # Se une la palabra a buscar con el tipo de archivos que se buscan
        term = self.word_search + str("%20filetype:") + self.filetype if len(self.filetype) > 0 else self.word_search
        
        # Se carga la pagina
        url = self.URL.format(term, indx_page)
        print("")
        print("------------------------------------------------------------")
        print(url)

        time.sleep(2)
        
        headers = {'User-Agent': random.choice(self.user_agent)}
        page = requests.get(url, cookies={}, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Se cogen los resultados
        # Se coge el contenedor donde se guardan las búsquedas
        cont_results = soup.find(id="b_results")
        # Extraer las URL de los resultados de búsqueda
        url_elements = cont_results.find_all("a", class_="tilk")

        results = []
        for url_element in url_elements:
            link_url = url_element["href"]
            name_url = url_element.find_all("div", class_="tptt")[0].text.strip()
            print(f"Nombre: {name_url} \t URL: {link_url}")
            dict_url = {"Nombre": name_url, "URL": link_url, "Pagina":int (indx_page/10 + 1)}
            results.append(dict_url)

        return results

    def make_search_page_limit(self):
        # Se sabe qué páginas exactas se quieren visitar
        # El valor de la página se debe multiplicar *10
        results = []
        
        for page in self.list_pages:
            index_page = page * 10
            results_page = self.load_results(index_page)
            results.extend(results_page)

        return results

    def make_search_no_page_limit(self):
        # Se quieren todas las páginas
        results = []
        actual_page = 0

        while True:
            index_page = actual_page * 10
            results_page = self.load_results(index_page)

            if len(results_page) == 0:
                # No quedan más páginas
                break

            results.extend(results_page)
            actual_page += 1

        return results

    def make_search (self):
        # La busqueda se puede realizar para unas páginas limitadas o para todas

        results = []
        if len(self.list_pages) > 0:
            # El número de páginas a buscar esta limitado
            results = self.make_search_page_limit()
        else:
            # Se quieren los resultados de todas las páginas
            results = self.make_search_no_page_limit()

        return results

    def save_results (self, results):
        # Primero hay que cambiar el formao de self.pages por no admitirse ":" en la ruta de archivo
        pages = str(self.pages).replace(":", "-")
        with open(f"results/data_{self.word_search}_{self.filetype}_{pages}.json", "w") as file:
            json.dump(results, file, indent=3)


    def search_bing (self):
        # Lo primero es determinar qué páginas quiere visitar el usuario
        self.define_pages()

        # Una vez se conoce qué quiere buscar, se realiza la busqueda
        results = self.make_search()

        # Ya se tiene una lista de diccionarios con las URL, se guarda en un JSON
        self.save_results(results)



# Se lee el JSON, y para cada elemento se busca el resultado de esa busqueda
# Este resultado se guarda en data_"word_search"_"filetype"_"pages".json
with open("data_in.json", "r") as file:
    json_list = json.load(file)

for json_element in json_list:
    # Se crea el objeto de la clase Scrapper_bing
    scraper = Scrapper_bing(json_element["word_search"], json_element["filetype"], json_element["pages"])

    # Ahora se llama a la función encargada de realizar la búsqueda
    scraper.search_bing()

    time.sleep(4)