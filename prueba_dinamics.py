import requests 
 
url = 'https://angular.io/' 
 
response = requests.get(url) 
 
html = response.text 
 
print(html)