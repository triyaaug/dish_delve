import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.foodnetwork.com/recipes/recipes-a-z"  # URL of the cooking website to scrape
#response = requests.get(url)

#for when chromedriver is not in PATH
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--ssl-version-max=tls1.2')
driver = webdriver.Chrome(options=options)



#driver = webdriver.Chrome()
driver.get(url)
page = driver.page_source
soup = BeautifulSoup(page, 'lxml')

#get rid of popup
popup = WebDriverWait(driver, 5).until( 
    EC.element_to_be_clickable((By.CLASS_NAME, "o-InternationalDialog__a-Button--Text"))
)
popup.click()

list = soup.find('ul', class_='o-IndexPagination__m-List') #links of all recipes list according to letter
links = list.find_all('a', class_='o-IndexPagination__a-Button')

for link in links:
    print(link['href'])
    try:
        # Wait for the element to be clickable before clicking it
        print("link reached yippeee")
        link_element = driver.find_element(By.LINK_TEXT, link.text)
        link_element.click()

        new_page = driver.page_source
        new_soup = BeautifulSoup(new_page, 'lxml')

        title_element = new_soup.find('h3', class_='o-Capsule__a-Headline')

        # Check if the 'title_element' exists and then extract the text
        if title_element:
            title = title_element.find('span', class_='o-Capsule__a-HeadlineText')
            if title:
                title_text = title.text
                print("Title:", title_text)
        else:
            print("Title element not found")

        """"""
        if 'chicken' in new_soup:
            print(f"woooo the word chicken is here in {link['href']}")
        else:
            print("no chicken :(")
         
        
        driver.back()
    except NoSuchElementException:
        print("link not found womp womp")



"""
for link in links:
    print(link['href'])
   
    if 'chicken' in link['href']:
        print(f"woooo the word chicken is here in {link['href']}")
    else:
        print("no chicken :(")
    
    
"""

driver.close()


"""
if response.status_code == 200:
    print(links)
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
"""
