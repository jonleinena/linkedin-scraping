from calendar import month
import time

import selenium
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller
from logs import logger_config as logger
from datetime import datetime as dt
import pandas as pd



def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--headless")

    DRIVER = selenium.webdriver.Edge(options=chrome_options)
    return DRIVER

def search_linkedin_offers(DRIVER, data):

    #Search for offers in linkedin and save job ids for further scraping
    res_count = int(DRIVER.find_element(By.XPATH, '//*[@id="main-content"]/div/h1/span[1]').text)
    
    job_listings = []
    try:
        #done to scroll down and scrape all listings
        while(len(job_listings) < (res_count - 1)):
            job_listings+=(DRIVER.find_elements(By.XPATH, '//*[@id="main-content"]/section[2]/ul/li'))
            DRIVER.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        
        for i in range(0, len(job_listings)):
            
            job_id = str((job_listings[i].find_element(By.CLASS_NAME, 'base-card').get_attribute("data-entity-urn"))).split(':')[3]
            
            if(job_id not in data):
                #Declare dictionary that goes as each offer's id value. Keeps all info of the offer
                offer_data = {'job-id': "",
                            'job-title' : "",
                            'company-name' : "",
                            'location': "",
                            'job-description': "",
                            'offer-link': "",
                            'coverletter-path': "",
                            'suitable': ""
                            }
                
                logger.info(str(dt.now()) + " - [CURRENT SCRAPING JOB ID] "+ str(job_id))
                job_link = job_listings[i].find_element(By.CLASS_NAME, 'base-card__full-link').get_attribute("href")
                #assign empty offer data dict to each id
                
                data[job_id]=offer_data

                #update in the id values at the main dict its id & link
                (data[job_id])['offer-link'] = job_link
                data[job_id]["job-id"] = job_id
                
    except Exception as e:
        logger.error(str(dt.now()) + " - [SCRAPING LINKS] " + str(e))
    finally:
        logger.info(str(dt.now()) + " - [SCRAPING LINKS] Finished\n")
        
          
    
def scrape_linkedin_offers(DRIVER, data: dict):
    #saves the info of the offer in the dictionary
    
    try:
        #iterate over dictionary
        for job_id in data:
            #access each position to scrape & save info of offer
            current_offer = data[job_id]

            DRIVER.get(current_offer['offer-link'])
            
            time.sleep(5)
            job_title = DRIVER.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h1').text
            (data[job_id])['job-title'] = str(job_title)
            company = DRIVER.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a').text
            (data[job_id])['company-name'] = str(company)
            location = DRIVER.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[2]').text
            (data[job_id])['location'] = str(location)
            description = DRIVER.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div').text
            (data[job_id])['job-description'] = str(description)
            logger.info(str(dt.now()) + " - [SCRAPED] id:" +str(job_id) + "\n")
    except Exception as e:
        logging.error(str(dt.now()) + " - [SCRAPING OFFER] id: "+ "\n" +str(data[id]) + str(e))
        
    finally:
        logging.info(str(dt.now()) + " - [SCRAPING OFFER] Finished\n")


