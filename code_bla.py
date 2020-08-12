import dryscrape
from bs4 import BeautifulSoup
session = dryscrape.Session()
session.visit(my_url)
response = session.body()
soup = BeautifulSoup(response)