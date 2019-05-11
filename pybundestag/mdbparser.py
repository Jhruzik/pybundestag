#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#Import Modules#
from bs4 import BeautifulSoup
import pandas as pd
import json


#Read in XML File#
def read_mdbs(path):
    """Reads in data on members of the Bundestag 
    as BeautifulSoup
    
    This function uses master data on members of the 
    German Bundestag in raw XML format and converts it 
    into a more easy to parse format by utilizing 
    BeautifulSoup and the lxml parser.
    
    The Input has to be the path to the master data as
    provided by the Bundestag in raw XML format.
    
    Parameters
    -----------
    path : string
        The path to the master data as provided by the
        Bundestag. Must be a valid xml file.
        
    Returns
    -----------
    soup : BeautifulSoup
        A BeautifulSoup object used for further parsing.
    """
    with open(path, mode = "r", encoding = "utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")
        mdbs = soup.find_all("mdb")
        return(mdbs)
        
#Get Personal Information of single MDB#
def parse_personal(mdb):
    #Parse#
    try:
        personalid = mdb.find("id").get_text()
    except Exception:
        personalid = None
    #Parse First Name#
    try:
        firstname = mdb.find("vorname").get_text()
    except Exception:
        firstname = None
    #Parse Last Name#
    try:
        lastname = mdb.find("nachname").get_text()
    except Exception:
        lastname = None
    #Parse Academic Title#
    try:
        acad = mdb.find("akad_titel").get_text()
        if acad == "":
            acad = None
    except Exception:
        acad = None
    #Parse Year of Birth#
    try:
        birthyear = mdb.find("geburtsdatum").get_text()
    except Exception:
        birthyear = None
    #Parse Place of Birth#
    try:
        birthplace = mdb.find("geburtsort").get_text()
    except Exception:
        birthplace = None
    #Parse Year of Death#
    try:
        death = mdb.find("sterbedatum").get_text()
        if death == "":
            death = None
    except Exception:
        death = None
    #Parse Gender#
    try:
        gender = mdb.find("geschlecht").get_text()
    except Exception:
        gender = None
    #Parse Party#
    try:
        party = mdb.find("partei_kurz").get_text()
    except Exception:
        party = None
    #Parse Occupation#
    try:
        occupation = mdb.find("beruf").get_text()
        if occupation == "":
            occupation = None
        else:
            occupation = occupation.split(", ")
    except Exception:
        occupation = None
    #Parse Vita#
    try:
        vita = mdb.find("vita_kurz").get_text()
    except Exception:
        vita = None
    
    #Collect to Dict#
    personal_dict = {
            "id" : personalid,
            "firstname" : firstname,
            "lastname" : lastname,
            "name" : " ".join([firstname, lastname]),
            "academic" : acad,
            "birthyear" : birthyear,
            "birthplace" : birthplace,
            "deathyear" : death,
            "gender" : gender,
            "party" : party,
            "occupation" : occupation,
            "vita" : vita
            }
    
    return(personal_dict)
    
#Look Up Plenary Period Specific Information for MdB#
def parse_period(personalid, period, mdbs, institutions = None):
    #Convert Input to str#
    personalid = str(personalid)
    period = str(period)
    #Filter List of MdBs to personalid#
    try:
        mdb_result = [x for x in mdbs if x.find("id").get_text() == personalid][0]
    except IndexError:
        raise ValueError("Argument personalid does not exist")
    #Filter List of Plenary Periods to period#
    periods_mdb = mdb_result.find_all("wahlperiode")
    try:
        period_result = [x for x in periods_mdb if x.find("wp").get_text() == period][0]
    except IndexError:
        raise ValueError("MdB seems not be part of Plenary Period")
    #Extract Information for given Period#
    #Electoral District#
    try:
        district = period_result.find("wkr_name").get_text()
        if district == "":
            district = None
    except Exception:
        district = None
    #Mandate#
    try:
        mandate = period_result.find("mandatsart").get_text()
    except Exception:
        mandate = None
    #List#
    try:
        elec_list = period_result.find("liste").get_text()
    except Exception:
        elec_list = None
    #Check for Institution Membership#
    if type(institutions) is list:
        membership_dict = dict()
        try:
            mdb_institutions = [x.get_text() for x in period_result.find_all("ins_lang")]
        except:
            mdb_institutions = []
        for institution in institutions:
            if institution in mdb_institutions:
                membership_dict[institution] = True
            else:
                membership_dict[institution] = False
    elif type(institutions) is not None:
        raise ValueError("institutions should either be a list or None")
    
    #Collect to Result Dict#
    result_dict = {
            "period" : period,
            "district" : district,
            "mandate" : mandate,
            "list" : elec_list,
            }
    #Add Institution Membership if present#
    try:
        for institution in membership_dict:
            result_dict[institution] = membership_dict[institution]
    except:
        pass
    
    return(result_dict)