from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import html5lib

# NOTES
# You have to solve a reCaptcha to enter the site at the first
# In this code the scraper collects 250 resumes per field. You can increase it by changing the range in line-40

# Fill this list with the fields
myfields = ["python","java","dot net"]
baseurl = "https://resumes.indeed.com/"
driver = webdriver.Chrome()
driver.get(baseurl)
for ele,field in enumerate(myfields):
    count = 0
    myfield = driver.find_element_by_xpath('//*[@id="input-q"]')
    myfield.send_keys(Keys.CONTROL + "a")
    myfield.send_keys(Keys.DELETE)
    myfield.send_keys(field)
    if ele == 0:               
        driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div[2]/div/form/div[3]/button').click()
    else:
        driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div[1]/div[1]/div/form/div[3]/button').click()
    
    # For reCaptcha - Indeed is asking only once(for one field)
    try:
        # this waits for 180sec or until the presence of given element is detected
        element = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[2]/div/div[2]/div[2]/div[1]/div/div[1]/span[1]/a'))
        )
    finally:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html5lib')
        pages = soup.find('div',{'class':'rezemp-ResumeSearchPage-Pagination icl-Grid-col icl-u-xs-span12 icl-u-md-span7'})
        print(len(pages))
        for index in range(5):
            divs = []
            if index == 0:
                pass
            elif index == 1:
                driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div[5]/span[14]').click()
            else:  
                driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div[5]/span[15]').click()

            for div in soup.find('div',{'class':'icl-Grid-col icl-u-xs-span12 icl-u-md-span7 icl-Body'}):
                divs.append(div)
            for i in range(1,len(divs)+1):
                window_before = driver.window_handles[0]
                driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div[2]/div[{}]/div/div[1]/span[1]/a'.format(i)).click()
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                hm = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div/div[2]/div/div')
                mytext = hm.text
                with open("Resumes/{0}-{1}.txt".format(field,i+count),"w") as textfile:
                    textfile.write(mytext)
                driver.close()
                driver.switch_to_window(window_before)  
            count += len(divs)

# This line closes the head-less browser that is opened
driver.close()