from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import html5lib

# NOTES
# You have to solve a reCaptcha to enter the site at the first
# For now this scraper collects 250 resumes per field. You can increase it by changing the range in line-38

# Fill this list with the fields
myfields = ["dot net"]
count = 0
baseurl = "https://resumes.indeed.com/"
driver = webdriver.Chrome()
driver.get(baseurl)
for field in myfields:
    myfield = driver.find_element_by_xpath('//*[@id="input-q"]')
    myfield.send_keys(Keys.CONTROL + "a")
    myfield.send_keys(Keys.DELETE)
    myfield.send_keys(field)
    if count == 0:               
        driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[1]/div[2]/div/form/div[3]/button').click()
    else:
        driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div[1]/div[1]/div/form/div[3]/button').click()
        
    try:
        element = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[2]/div/div[2]/div[2]/div[1]/div/div[1]/span[1]/a'))
        )
    finally:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html5lib')
        pages = soup.find('div',{'class':'rezemp-ResumeSearchPage-Pagination icl-Grid-col icl-u-xs-span12 icl-u-md-span7'})
        print(len(pages))
        pagenum = 0
        for index in range(5):
            url = []
            if pagenum == 0:
                pass
            else:
                driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div[2]/div[5]/span[{}]/span'.format(pagenum)).click()
            for link in soup.find('div',{'class':'icl-Grid-col icl-u-xs-span12 icl-u-md-span7 icl-Body'}):
                url.append(link)
            for i in range(1,len(url)+1):
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
            if pagenum == 3 or pagenum == 0:
                pagenum += 3
            else:
                pagenum += 2
            count += len(url)
driver.close()