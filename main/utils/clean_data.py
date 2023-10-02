import os
import logging
from datetime import datetime as dt
import re

regex = re.compile('[^a-zA-ZáéíóúüÁÉÍÓÚÜñÑ()]+')


#Deletes file from system
#all files containing invalid coverletters will be deleted for optimization's sake
#@param path: path to file
def delete_file(path):
    try:
        if(os.path.exists):
            os.remove(path)
        else:
            logging.warning(str(dt.now()) + " - [FILE DOES NOT EXIST] path: "+ str(path))
    except FileNotFoundError or IOError as e:
        logging.exception(str(dt.now()) + " - [DELETING FILE] path: "+ str(path) + " " +str(e))

#will clean the coverletter path from the main dict (to be dumped then into the json)
#@param id_array: list with ids of job listings to delete
#@param data: dict with all the data
def clean_files(id_array, data):
    for element in id_array:
        delete_file(data[element]['coverletter-path'])
        data[element]['coverletter-path'] = ''
        data[element]['suitable'] = 'no'
        logging.info(str(dt.now()) + " - [OFFER UPDATED] id: "+ str(element))

def read_files(data):
    id_array = []
    for id, info in data:
        try:
            file = open(info['coverletter-path'] ,'r')
            text = file.read()

            if(len(text) < 40 or bool(re.search(regex, text))):
                id_array.append(id)
            else:
                pass
        except FileNotFoundError or IOError as e:
            logging.exception(str(dt.now()) + " - [COULD NOT READ FILE] path: "+ str(info['coverletter-path']) + " " +str(e))
    
    return id_array
