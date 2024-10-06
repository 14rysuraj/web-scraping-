from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--lang=en")



driver = webdriver.Chrome(options=chrome_options)


driver.get("https://www.google.com/?hl=en")


search_box = driver.find_element(By.XPATH, "//textarea[contains(@class,'gLFyf')]")
search_box.send_keys("agro tech in Nepal")
search_box.send_keys(Keys.RETURN)
time.sleep(5)

button= driver.find_elements(By.XPATH, "//a[contains(@class,'jRKCUd')]")
if button:
    button[0].click()
time.sleep(5)



data={'Business Map Link':[],'Name of Business':[],'Rating of the business in the Gmap':[],'No of rating':[],'Type of Business':[],'phone no':[],'Website mentioned':[]}

results=driver.find_elements(By.XPATH,"//div[contains(@class,'VkpGBb')]")

print(len(results))





# scrollable_div = driver.find_element(By.XPATH, "//div[@class='m6QErb DxyBCb kA9KIf dS8AEf XiKgde ecceSd']")


# max_scroll = 4
# scroll_increment=200
# for i in range(max_scroll):
#     driver.execute_script("arguments[0].scrollTop = arguments[1].scrollHeight", scrollable_div)
#     time.sleep(5)



# # results =

# print(f"Total results found: {len(results)}")

# count=0
# for i, result in enumerate(results):
#     try:
#         result.click()
#         time.sleep(5)
#         count+=1
#         print(count)

        
#     except:
#         print(f"Result {i+1}: Name not found")

# print(f"Total count :{count}")
# driver.quit()




