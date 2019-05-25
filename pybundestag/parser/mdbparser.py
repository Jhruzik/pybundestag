#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Import Modules
from bs4 import BeautifulSoup
import itertools
import pandas as pd
import json


# Read in XML File
def read_mdbs(path):
    """Reads in data on members of the Bundestag 
    as BeautifulSoup
    
    This function uses master data on members of the 
    German Bundestag in raw XML format and converts it 
    into a more easy to parse format by utilizing 
    BeautifulSoup and the lxml parser.
    
    Parameters
    -----------
    path : string
        The path to the master data as provided by the
        Bundestag. Must be a valid XML file.
        
    Returns
    -----------
    mdbs : BeautifulSoup
        A BeautifulSoup object used for further parsing.
        Contains all MdBs in file.
    """
    with open(path, mode = "r", encoding = "utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")
        mdbs = soup.find_all("mdb")
        return(mdbs)
        
# Get Personal Information of Single MDB
def parse_personal(mdb):
    """Get personal information of a single MdB
    
    Given a single MdB as input, this function will yield
    a dictionary with personal information. This also 
    includes the name, gender, CV, and more
    information.
    
    Parameters
    -----------
    mdb: BeautifulSoup
        A single element of read_mdbs output, representing
        a single member of the German Bundestag.
        
    Returns
    -----------
    personal_dict: Dict
        A dictionary containing personal information on
        a single member of the German Bundestag. This
        includes a unique ID, name, academic title,
        year of birth, place of birth, year of death,
        gender, party affiliation, occupation,
        parliamentary periods and a short CV.
    """
    # Parse Id
    try:
        personalid = mdb.find("id").get_text()
    except Exception:
        personalid = None
    # Parse First Name
    try:
        firstname = mdb.find("vorname").get_text()
    except Exception:
        firstname = None
    # Parse Last Name
    try:
        lastname = mdb.find("nachname").get_text()
    except Exception:
        lastname = None
    # Parse Academic Title
    try:
        acad = mdb.find("akad_titel").get_text()
        if acad == "":
            acad = None
    except Exception:
        acad = None
    # Parse Year of Birth
    try:
        birthyear = mdb.find("geburtsdatum").get_text()
    except Exception:
        birthyear = None
    # Parse Place of Birth
    try:
        birthplace = mdb.find("geburtsort").get_text()
    except Exception:
        birthplace = None
    # Parse Year of Death
    try:
        death = mdb.find("sterbedatum").get_text()
        if death == "":
            death = None
    except Exception:
        death = None
    # Parse Gender
    try:
        gender = mdb.find("geschlecht").get_text()
    except Exception:
        gender = None
    # Parse Party
    try:
        party = mdb.find("partei_kurz").get_text()
    except Exception:
        party = None
    # Parse Occupation
    try:
        occupation = mdb.find("beruf").get_text()
        if occupation == "":
            occupation = None
        else:
            occupation = occupation.split(", ")
            occupation = ";".join(occupation)
    except Exception:
        occupation = None
    # Parse Parliamentary Periods
    try:
        period = mdb.find_all("wp")
        period = [x.get_text() for x in period]
        period = ";".join(period)
    except Exception:
        period = None
    # Parse Vita
    try:
        vita = mdb.find("vita_kurz").get_text()
    except Exception:
        vita = None
    
    # Collect to Dict
    personal_dict = {
            "ID" : personalid,
            "FirstName" : firstname,
            "LastName" : lastname,
            "Name" : " ".join([firstname, lastname]),
            "AcademicTitle" : acad,
            "BirthYear" : birthyear,
            "BirthPlace" : birthplace,
            "DeathYear" : death,
            "Gender" : gender,
            "Party" : party,
            "Occupation" : occupation,
            "Period" : period,
            "Vita" : vita
            }
    
    return(personal_dict)
    
# Look Up Plenary Period Specific Information for MdB
def parse_period(mdb, period, institutions = None):
    """Gather period specific data for a MdB
    
    Given a single mdb and a parliamentary period,
    this function will return information specific 
    to that MdB during the specified parliamentary
    period. This includes the MdB's electoral
    district, mandate type and electoral list.
    
    You can also check, if the MdB was a member of
    one or more institutions. This might include 
    committees or factions.
    
    Parameters
    -----------
    mdb: BeautifulSoup
        A single element of read_mdbs output, representing
        a single member of the German Bundestag.
        
    period: int
        The parliamentary session you want information
        for.
        
    institutions: list of str [optional]; default: None
        A list of institutions to check for whether or
        not the MdB was a member in during the
        parliamentary period.
        
    Returns
    -----------
    period_dict: Dict
        A dictionary containing period specific
        information for an MdB. This information
        includes the electoral district,
        mandate type, and electoral list. If a
        list of institutions was defined, there
        will be a key for every institution in the
        form of 'member_*' where the asteriks is a
        placeholder for the institution. True
        implies that the MdB was a member of that
        institution during the period, while False
        would impy otherwise.
    """
    # Convert Input to str
    period = str(period)
    # Filter List of Parliamentary Periods to Period
    periods_mdb = mdb.find_all("wahlperiode")
    try:
        period_result = [x for x in periods_mdb if x.find("wp").get_text() == period][0]
    except IndexError:
        raise ValueError("MdB seems not be part of parliamentary period")
    # Extract Information for given Period
    # Electoral District
    try:
        district = period_result.find("wkr_name").get_text()
        if district == "":
            district = None
    except Exception:
        district = None
    # Mandate
    try:
        mandate = period_result.find("mandatsart").get_text()
    except Exception:
        mandate = None
    # List
    try:
        elec_list = period_result.find("liste").get_text()
    except Exception:
        elec_list = None
    # Check for Institution Membership
    if type(institutions) is list:
        membership_dict = dict()
        try:
            mdb_institutions = [x.get_text() for x in period_result.find_all("ins_lang")]
        except:
            mdb_institutions = []
        for institution in institutions:
            if institution in mdb_institutions:
                membership_dict["member_"+institution] = True
            else:
                membership_dict["member_"+institution] = False
    elif institutions is not None:
        raise ValueError("Institutions should either be a list or None")
    
    # Collect to Result Dict
    period_dict = {
            "Period" : period,
            "District" : district,
            "Mandate" : mandate,
            "List" : elec_list,
            }
    # Add Institution Membership if present
    try:
        for institution in membership_dict:
            period_dict[institution] = membership_dict[institution]
    except:
        pass
    
    # Return Result
    return(period_dict)
    
    
# Reduce List of MdBs to a certain Parliamentary Period
def _reduce_to_period(mdbs, period):
    # Convert Period to String
    period = str(period)
    # Convert mdbs to List of Period Lists
    period_list = [x.find_all("wp") for x in mdbs]
    def _get_period(l):
        l_new = [x.get_text() for x in l]
        return(l_new)
    period_list = [_get_period(x) for x in period_list]
    # Filter out MdBs that do not belong to specified Period
    period_boolean = [period in x for x in period_list]
    mdbs_filtered = list(itertools.compress(mdbs, period_boolean))
    return(mdbs_filtered)
    
# Parse all MdBs in File
def collect_mdbs(mdbs, output = "dataframe", period = None, institutions = None):
    """Collects all MdBs of MdB list into either 
       a dataframe, json, or list.
    
    Using this function, you can collect all the 
    MdBs in read_mdbs' output into a pandas 
    DataFrame, a json string, or a  python list. 
    This data can be used for further analysis.
    
    Parameters
    -----------
    mdbs: BeautifulSoup
        Output from read_mdbs function.
        
    output: string
        Either 'dataframe', 'json', or 'list'.
        'dataframe' will result in a pandas
        DataFrame. 'json' will be a json
        string and 'list' is a Python list
        of dictionaries. Defaults to
        'dataframe'
        
    period: int [optional]
        If you want to collect data only for a
        certain parliamentary period, you can 
        specify this period as an integer.
        
    institutions: list of str [optional]
        You can include dummy variables for membership
        in certain institutions. This must be a list
        of strings. Note that no sanity checks
        are made, so make sure that your spelling
        is correct. Can only be used if you have
        also specified a period.
        
    Returns
    -----------
    result: DataFrame, str, or list
        The output will depend on the value of
        the output argument. If set to 'dataframe',
        a pandas DataFrame is returned. If set to
        'json' a json string will be returned. 
        'list' will result in a Python list of
        dictionaries.
    """
    # React to Presence of Period
    if period is not None:
        # Convert Number to String
        period = str(period)
        # Filter out Irrelevant MdBs
        mdbs = _reduce_to_period(mdbs, period)
    # Init List to collect Results
    result_list = []
    # Parse Single MdB and add to result_list
    for mdb in mdbs:
        try:
            personal_dict = parse_personal(mdb)
            if period is not None:
                period_dict = parse_period(mdb = mdb,
                                           period = period,
                                           institutions = institutions)
            else:
                period_dict = {}
            mdb_dict = {**personal_dict, **period_dict}
            result_list.append(mdb_dict)
        except ValueError:
            pass
    # Write Results to desired Output Format
    if output == "dataframe":
        result = pd.DataFrame(result_list)
    elif output == "json":
        result = json.dumps(result_list, ensure_ascii = False, indent = 1)
    elif output == "list":
        result = result_list
    else:
        raise ValueError("Output must either be 'dataframe', 'json', or 'list'.")
        
    return(result)