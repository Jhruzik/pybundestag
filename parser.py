#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import Modules#
from bs4 import BeautifulSoup
import pandas as pd

#Read in XML File#
def read_protocol(path):
    with open(path, mode = "r", encoding = "utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    return(soup)


#Get Overall Information#
def get_metadata(soup):
    try:
        period = soup.find("wahlperiode").get_text()
    except Exception:
        period = None
    try:
        session = soup.find("sitzungsnr").get_text()
    except Exception:
        session = None
    try:
        location = soup.find("ort").get_text()
    except:
        location = None
    try:
        date = soup.find("datum")["date"]
    except Exception:
        date = None
    return_dict = {"location" : location,
                   "date" : date,
                   "period" : period,
                   "session" : session}
    return(return_dict)

#Parse Single Speech#
def parse_speech(speech):
    
    #Parse Information regarding Speaker#
    try:
        speaker = speech.find("redner")
        try:
            firstname = speaker.find("vorname").get_text()
        except Exception:
            firstname = ""
        try:
            lastname = speaker.find("nachname").get_text()
        except Exception:
            lastname = ""
        try:
            party = speaker.find("fraktion").get_text()
        except Exception:
            party = None
        try:
            role = speaker.find("rolle").get_text()
        except Exception:
            role = None
        speaker_dict = {"firstname" : firstname,
                        "lastname" : lastname,
                        "name" : firstname + " " + lastname,
                        "party" : party,
                        "role" : role}
    except Exception:
        speaker_dict = {"firstname" : None,
                        "lastname" : None,
                        "name" : None,
                        "party" : None,
                        "role" : None}
    
    #Parse Text of Speech#
    try:
        text = speech.find_all("p", {"klasse" : ["J", "J_1", "O"]})
        text = "\n".join([x.get_text() for x in text])
    except Exception:
        text = None
    
    #Return Information in Dictionary
    return_dict = {"Speaker" : speaker_dict["name"], "Party" : speaker_dict["party"], "text" : text}
    return(return_dict)
    
    
#Parse all Speeches in File#
def speeches_to_df(soup):
    result_list = []
    meta = get_metadata(soup)
    for speech in soup.find_all("rede"):
        result = parse_speech(speech)
        result["location"] = meta["location"]
        result["date"] = meta["date"]
        result["period"] = meta["period"]
        result["session"] = meta["session"]
        result_list.append(result)
    result_df = pd.DataFrame(result_list)
    return(result_df)