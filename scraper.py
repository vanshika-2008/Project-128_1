from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv

start_url = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'
browser = webdriver.Chrome('chromedriver.exe')
browser.get(start_url)
time.sleep(10)
headers = ['Name','Light_years_from_Earth','Planet_Mass','Stellar_Magnitude','Discovery_Year','Hyperlink','Planet_Type','Planet_Radius','Orbital_Radius','Orbital_Period','Eccentricity']
planet_data = []
new_planet_data = []
def scrape() :
    for i in range(0,490) :
        Soup = BeautifulSoup(browser.page_source,'html.parser')
        for ul_tag in Soup.find_all('ul',attrs={'class','exoplanet'}) :
            li_tags = ul_tag.find_all('li')
            temp_list = []
            for index,li_tag in enumerate(li_tags) :
                if index == 0 :
                    temp_list.append(li_tag.find_all('a')[0].contents[0])
                else :
                    try :
                        temp_list.append(li_tag.contents(0))
                    except :
                        temp_list.append('')

            hyperlink_li_tag = li_tags[0]
            temp_list.append('https://exoplanets.nasa.gov'+hyperlink_li_tag.find_all('a',href = True)[0]['href'])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
def scrape_more_data(hyperlink) :
    try :
        page= requests.get(hyperlink)
        soup = BeautifulSoup(page.content,'html.parser')
        temp_list = []
        for tr_tag in soup.find_all('tr',attrs={'class':'fact_row'}) :
            td_tags = tr_tag.find_all('td')
            for td_tag in td_tags :
                try :
                    temp_list.append(td_tag.find_all('div',attrs= {'class':'value'})[0].contents[0])
                except :
                    temp_list.append('')
        new_planet_data.append(temp_list)
    except :
        time.sleep(1)
scrape()
for index,data in enumerate(planet_data) :
    scrape_more_data(data[5])

final_planet_data = []
for index, data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [i.replace('\n','') for i in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data+new_planet_data_element)     
    
file = open('scraper2.csv','w')
csv_writer = csv.writer()
csv_writer.writerow(headers)
csv_writer.writerows(planet_data)



