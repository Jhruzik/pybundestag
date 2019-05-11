#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import Modules#
from bs4 import BeautifulSoup
import pandas as pd
import json

#Read in XML File#
def read_protocol(path):
    """Reads in protocols as BeautifulSoup
    
    This function uses protocols of the German Bundestag
    in raw XML format and converts them into a more
    easy to parse format by utilizing BeautifulSoup and
    the lxml parser.
    
    The Input has to be the path of a Bundestag protocol
    in raw XML format. Make sure that it was published
    during or after the 19th plenary period. Older XML
    files can not be parsed due to very little structure.
    
    Parameters
    -----------
    path : string
        The path to the specific Bundestag protocol you
        would like to parse. Must be a valid xml file.
        
    Returns
    -----------
    soup : BeautifulSoup
        A BeautifulSoup object used for further parsing.
    """
    with open(path, mode = "r", encoding = "utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    return(soup)


#Get Overall Information#
def parse_metadata(soup):
    """Parse meta data from protocol
    
    If you would like to parse meta data from a given
    protocol, you can use this function. It will yield
    the plenary period, plenary session, location and
    the date of the session the protocol was compiled
    for.
    
    Parameters
    -----------
    soup: BeautifulSoup
        The output of read_protocol. In order to
        extract the desired meta data, you will have
        to parse the protcol by using read_protocol
        first. The output of that function should be
        the input to this function.
    
    Returns
    -----------
    return_dict: Dictionary
        A dictionary having the keys: location,
        date, period, and session. Values will be
        None if no information was found.
    """
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
    """Split information on speaker and text of speech
    
    This function will yield the first name, last name,
    party and role of a speaker as well as the text of
    his/her speech. This way, you will obtain the raw
    speech without any comments and some meta data of
    the speaker.
    
    Parameters
    -----------
    speech: BeautifulSoup
        Use a single speech extracted from the entire
        protocol converted by read_protocol.
        
    Returns
    -----------
    return_dict: Dictionary
        A dictionary containing the keys: Speaker,
        Party, and Text. Speaker is the concatenation 
        of the first name and last name. Party represents
        the party affiliation of the speaker. Text is the
        raw speech stripped of all comments.
    """
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
    return_dict = {"Speaker" : speaker_dict["name"], "Party" : speaker_dict["party"], "Text" : text}
    return(return_dict)
    
    
#Parse all Speeches in File#
def collect_speeches(soup, output = "dataframe", metadata = False):
    """Collect all speeches into either a dataframe, json, or list
    
    After converting a given protocol with read_protocol,
    you can collect all speeches (plus additional meta data)
    into a dataframe, json, or list.
    
    The result is highly structured and can be used for
    further analysis.
    
    Parameters
    -----------
    soup: BeautifulSoup
        The result of using read_protocol() on a 
        specific protocol.
    output: string ['dataframe', 'json', 'list']; default: 'dataframe'
        The desired output format. Could either be a pandas
        dataframe, a json string or a list.
    metadata: boolean; default: False
        Whether or not to include any meta data
        for the speeches to the result.
        
    Returns
    -----------
    result: Either pandas.DataFrame, str or list
        All speeches in a highly structured format.
        Will contain raw text and additional information
        on speaker and context.
    """
    result_list = []
    meta = parse_metadata(soup)
    for speech in soup.find_all("rede"):
        result = parse_speech(speech)
        if metadata:
            result["location"] = meta["location"]
            result["date"] = meta["date"]
            result["period"] = meta["period"]
            result["session"] = meta["session"]
        result_list.append(result)
    if output == "dataframe":
        result = pd.DataFrame(result_list)
    elif output == "json":
        result = json.dumps(result_list, ensure_ascii = False, indent = 1)
    elif output == "list":
        result = result_list
    else:
        raise ValueError("Output must either be 'dataframe', 'json', or 'list'.")
    return(result)