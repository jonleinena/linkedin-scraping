import main
from main.lib import gpt_code as gpt
from utils import clean_data as cd 
import os
import time
import json
from logs import logger_config as logger
from datetime import datetime as dt


data = { }



if __name__ == '__main__':
    try:

        DRIVER = main.create_driver()
        DRIVER.get("https://www.linkedin.com/jobs/search/?keywords=ML%20engineer&location=España&geoId=105646813&refresh=true")
        time.sleep(5)
        logger.info(str(dt.now()) + " - [MAIN] Starting scraping process")
        main.search_linkedin_offers(DRIVER, data)
        main.scrape_linkedin_offers(DRIVER, data)
        
        for job_id in data:
            
            logger.info(str(dt.now()) + " - [PROMPTING FOR COVER LETTER] id: "+ str(job_id))
            job_data = data[job_id]
            gpt.init_key()
            res = gpt.generate_responses(str(job_data['job-description']))
            job_data['coverletter-path'] = str( gpt.response_to_text( job_id, job_data['company-name'], res))
            logger.info(str(dt.now()) + " - [COVERLETTER WRITTEN] id: " + str(job_data['job-id']) + "\n")
            cd.clean_files( cd.read_files(data), data)


       
        json_object = json.dumps(data, indent=4)
        with open("../output/data.json", 'w') as dumpfile:
            dumpfile.write(json_object)
            logger.info(str(dt.now()) + " - [SAVING JSON]")
        
    except Exception as e:
        logger.error(str(dt.now()) + " - [MAIN] "+ str(e))
    finally:
        DRIVER.delete_all_cookies()
        DRIVER.quit()
        
        logger.info(str(dt.now()) + " - [Chrome cerrado]")