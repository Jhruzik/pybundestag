#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __name__ == "__main__":

    
    # Preliminaries

        # Import Modules
    import parser.speechparser
    import parser.mdbparser
    import argparse
    import os
    import re
    import json
    import pandas as pd

        # Parse User Arguments
    arg_parser = argparse.ArgumentParser(description='Parse Bundestag protocols and MdBs to CSV or JSON files')
    arg_parser.add_argument("entity", help = "The object to parse [protocol or mdb]")
    arg_parser.add_argument("input", help = "Input for parsing. If folder, all XML files are parsed")
    arg_parser.add_argument("output", help = "Output file. Should end in either .csv or .json")
    arg_parser.add_argument("-s", "--seperator", required = False, default = ",", 
                        help = "Seperator for csv File")
    arg_parser.add_argument("-m", "--meta", required = False, default = False,
                        help="Flag for whether or not meta data should be added",
                        action="store_true")
    arg_parser.add_argument("-p", "--period", required = False, default = None,
                            help = "Extract MdBs for parliamentary period")
    arg_parser.add_argument("-i", "--institutions", required = False, default = None,
                            help = "Check for MdB membership of specified institutions (seperated by ';')")
    args = arg_parser.parse_args()
    
    # Wrangle Arguments
    output_extension = re.search("(?<=\.)\w+$", args.output).group()
    args.entity = args.entity.lower()
    if args.institutions is not None:
        args.institutions = args.institutions.split(";")
    
        # Catch Bad User Input
            # Wrong Entity
    if args.entity not in ["protocol", "mdb"]:
        raise ValueError("entity should be protocol or mdb")
            # Wrong Output File Type
    if (args.output.endswith("csv") == False) & (args.output.endswith("json") == False):
        raise ValueError("Your output must end in either '.csv' or '.json'.")

        # Create List of Input Files
    if os.path.isdir(args.input):
        content = os.listdir(args.input)
        content = [os.path.join(args.input, x) for x in content if x.endswith(".xml")]
    elif (os.path.isfile(args.input)) and (args.input.lower().endswith(".xml")):
        content = []
        content.append(args.input)
    else:
        raise ValueError("Your input is not a xml file or a folder.")
    
        # Map internal output format to user input
    extension_dict = {"csv" : "dataframe", "json" : "json"}
    
    # Parse Protocols
    if args.entity == "protocol":

        # Parse if Input is Single File
        if len(content) == 1:
            # Read in Single Protocol and collect all Speeches
            protocol = parser.speechparser.read_protocol(content[0])
            speeches = parser.speechparser.collect_speeches(protocol,
                                                            output = extension_dict[output_extension],
                                                            metadata = args.meta)
            # Write CSV to Output Path
            if output_extension == "csv":
                speeches.to_csv(args.output, sep = args.seperator,
                                encoding = "utf-8", index = False)
            # Write JSON to Output Path
            elif output_extension == "json":
                with open(args.output, mode = "w", encoding = "utf-8") as f:
                    f.writelines(speeches)
            else:
                raise ValueError("Your output format {} is neither 'csv' or 'json'.".format(output_extension))
                
            # Exit with Success
            print("Speeches written to: {}".format(args.output))
                
        # Parse if Input is a Folder
        elif len(content) > 1:
            # Init Counter and Result List for Loop
            parser_count = 1
            conent_len = str(len(content))
            speeches_list = []
            for file in content:
                # Parse Single File and append Output to Result List
                print("\rParsing File: {} of {}".format(parser_count, conent_len), end = "")
                parser_count += 1
                protocol = parser.speechparser.read_protocol(file)
                speeches_tmp = parser.speechparser.collect_speeches(protocol, 
                                                                    output = "list", 
                                                                    metadata = args.meta)
                speeches_list.extend(speeches_tmp)
            # Write Result as CSV to Output Path
            if output_extension == "csv":
                result_df = pd.DataFrame(speeches_list)
                result_df.to_csv(args.output, sep = args.seperator, 
                                 encoding = "utf-8", index = False)
            # Write Result as JSON to Output Path
            elif output_extension == "json":
                with open(args.output, mode = "w", encoding = "utf-8") as f:
                    result = json.dumps(speeches_list, ensure_ascii = False, indent = 1)
                    f.writelines(result)
                    
            # Exit with Success
            print("\nSpeeches written to: {}".format(args.output))
            
        else:
            raise ValueError("Your output format {} is neither 'csv' or 'json'.".format(output_extension))

        

    # Parse MdBs
    if args.entity == "mdb":
        
        # Parse if Input is Single File
        if len(content) == 1:
            # Read in Single MdB List and collect all MdBs
            mdbs = parser.mdbparser.read_mdbs(content[0])
            mdbs = parser.mdbparser.collect_mdbs(mdbs = mdbs,
                                                 output = extension_dict[output_extension],
                                                 period = args.period,
                                                 institutions = args.institutions)
            # Write CSV to Output Path
            if output_extension == "csv":
                mdbs.to_csv(args.output, sep = args.seperator,
                            encoding = "utf-8", index = False)
            # Write JSON to Output Path
            elif output_extension == "json":
                with open(args.output, mode = "w", encoding = "utf-8") as f:
                    f.writelines(mdbs)
            else:
                raise ValueError("Your output format {} is neither 'csv' or 'json'.".format(output_extension))
                
        # Exit with Success
        print("MdBs written to: {}".format(args.output))