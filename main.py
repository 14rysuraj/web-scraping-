from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import re


phone_pattern = r'\d{2,3}-\d{6,7}'

chrome_options = Options()
chrome_options.add_argument("--lang=en")

driver = webdriver.Chrome(options=chrome_options)


driver.get("https://www.google.com/?hl=en")


search_box = driver.find_element(By.XPATH, "//textarea[contains(@class,'gLFyf')]")
search_box.send_keys("agro tech in Nepal")
search_box.send_keys(Keys.RETURN)

time.sleep(5)


button = driver.find_elements(By.XPATH, "//a[contains(@class,'jRKCUd')]")
if button:
    button[0].click()

time.sleep(5)


data = {
   
    'Name of Business': [],
    'Business Map Link': [],
    'Rating of the business in the Gmap': [],
    'No of rating': [],
    'Type of Business': [],
    'Phone no': [],
    'Website mentioned': [],
    'Location':[]
}

def ensure_equal_length():
    # Find the maximum length of the lists in the data dictionary
    max_len = max(len(lst) for lst in data.values())

    # Ensure all lists are of the same length
    for key in data:
        while len(data[key]) < max_len:
            data[key].append("NA")


def scrape_results():
    results = driver.find_elements(By.XPATH, "//div[contains(@class,'VkpGBb')]")
    print(f"Results found: {len(results)}")
    
    for i, result in enumerate(results):
       
        try:
            name = result.find_element(By.CLASS_NAME, "OSrXXb").text
            data['Name of Business'].append(name)
        except NoSuchElementException:
            data['Name of Business'].append("NA")


        try:
            element = result.find_element(By.XPATH, ".//a[@class='vwVdIc wzN8Ac rllt__link a-no-hover-decoration']")
            cid=element.get_attribute('data-cid')
            map_link = f"https://www.google.com/maps?cid={cid}"
            data['Business Map Link'].append(map_link)
        except NoSuchElementException:
            data['Business Map Link'].append("NA")


        try:
            rating_element = result.find_element(By.XPATH, ".//span[contains(@class,'yi40Hd YrbPuc')]")
            rating = rating_element.text
            data['Rating of the business in the Gmap'].append(rating)
        except NoSuchElementException:
            data['Rating of the business in the Gmap'].append("NA")
        
        try:
            no_of_rating=result.find_element(By.XPATH,".//span[contains(@class,'RDApEe YrbPuc')]").text
            data['No of rating'].append(no_of_rating)
        except NoSuchElementException:
            data['No of rating'].append("NA")

        try:
            child_element=result.find_element(By.XPATH,".//span[contains(@class,'Y0A0hc')]")
            upper_child_element=child_element.find_element(By.XPATH,"..")

            parent_element=upper_child_element.find_element(By.XPATH,"..")

            parent_text=parent_element.text
            

            child_text=child_element.text
            upper_child_text=upper_child_element.text
            business_type=parent_text.replace(child_text,'').strip()
            business_type=business_type.replace(upper_child_text,'').strip()
            business_type=business_type[2:]

            data['Type of Business'].append(business_type)
        except NoSuchElementException:
            data['Type of Business'].append("NA")

        try:
            
            phone_number=result.find_element(By.XPATH,".//div[contains(@class,'rllt__details')]/div[4]").text
            phone_number = phone_number.split('·')[-1].strip()
            if re.match(phone_pattern, phone_number):
                data['Phone no'].append(phone_number)
        except NoSuchElementException:
            data['Phone no'].append("NA")

        try:
            link_tag=result.find_element(By.XPATH,".//a[contains(@class,'yYlJEf Q7PwXb L48Cpd brKmxb')]")
            website=link_tag.get_attribute('href')
            data['Website mentioned'].append(website)
        except NoSuchElementException:
            data['Website mentioned'].append("NA")
        

        try:
            location=result.find_element(By.XPATH,".//div[contains(@class,'rllt__details')]/div[3]").text
            print(location)
            data['Location'].append(location)
        except NoSuchElementException:
            data['Location'].append("NA")

        ensure_equal_length()
    

        

        
            


    time.sleep(5)


scrape_results()


while True:
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@id,'pnnext')]")
        next_button.click()
        time.sleep(5) 
        scrape_results()
    except NoSuchElementException:
        print("No more pages.")
        break


df=pd.DataFrame(data)


df.to_excel("competitor_analysis.xlsx") 


driver.quit()
df
