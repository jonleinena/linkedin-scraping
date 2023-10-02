import openai
import os
import sys
import time
import logging
from datetime import datetime as dt

initial_instruction =  ""

def init_key():

    try:
        openai.api_key = os.environ('GPT_OPENAI_KEY')
        file = open("../data/GPTinstructions.txt", "r") 
        initial_instruction = file.read()
        file.close()
        logging.info(str(dt.now()) + " - [OPENAI KEY] read ok")
        logging.info(str(dt.now()) +" - [INITIAL INSTRUCTION] read ok")
        return initial_instruction

    except KeyError:
        logging.error(str(dt.now()) +"""
        You haven't set up your API key yet.
        
        If you don't have an API key yet, visit:
        
        https://platform.openai.com/signup

        1. Make an account or sign in
        2. Click "View API Keys" from the top right menu.
        3. Click "Create new secret key"

        Then, open the Secrets Tool and add OPENAI_API_KEY as a secret.
        """)
        exit(1)


def generate_responses(prompt):
    #function used to generate gpt3-5's responses
    
    try:
        response = openai.ChatCompletion.create(
        model=
        "gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": initial_instruction},
            {"role": "user", "content": str(prompt)}
        ], temperature = 1.5)
        logging.info(str(dt.now()) +" - [RESPONSE] generated ok")
        return(response['choices'][0]['message']['content'])
    except Exception as e:
        logging.error(str(dt.now()) +" - [RESPONSE]" + str(e))

def response_to_text(job_id, company_name, response):
    if (response != "It does not suit you. No cover letter provided."):
        try:
            file = open("../output/" + str(job_id) + "-"+str(company_name)+".txt", "w")
            file.write(response)
            file.close()
            logging.info(str(dt.now()) +" - [TEXT OUTPUT OK] id: "+ str(job_id))
            
            return("../output/" + str(job_id) + "-"+str(company_name)+".txt")

        except:
            logging.error(str(dt.now()) +" - [TEXT OUTPUT ERR] id: "+ str(job_id))
    else:
        return("../../output/not-suitable-" + str(job_id) + "-"+str(company_name)+".txt")