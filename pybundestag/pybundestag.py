
###Import Modules###
import speechparser
import argparse
import os
import re
import json
import pandas as pd

###Parse User Arguments###
parser = argparse.ArgumentParser(description='Process Arguments for Parsing of Bundestag Protocolls.')
parser.add_argument("-i", "--input", required = True, 
                    help = "Input for Parsing. If Folder, all XML Files are parsed")
parser.add_argument("-o", "--output", required = True,
                    help = "Output file. Should end in either .csv or .json")
parser.add_argument("-s", "--seperator", required = False, default = ",", 
                    help = "Seperator for csv File")
parser.add_argument("-m", "--meta", required = False, default = False,
                    help="increase output verbosity",
                    action="store_true")

args = parser.parse_args()

####TEMP INPUT FOR TESTING####
args.input = "/home/joshuahruzik/Entwicklung/pybundestag/Folder/"
args.output = "/home/joshuahruzik/test.json"
args.seperator = ","
args.meta = True

output_extension = re.search("(?<=\.)\w+$", args.output).group()




###Catch Bad User Input###
if (args.output.endswith("csv") == False) & (args.output.endswith("json") == False):
    raise ValueError("Your output must end in either '.csv' or '.json'.")


###Create List of Input Files###
if os.path.isdir(args.input):
    content = os.listdir(args.input)
    content = [args.input+x for x in content if x.endswith(".xml")]
elif (os.path.isfile(args.input)) and (args.input.endswith(".xml")):
    content = []
    content.append(args.input)
else:
    raise ValueError("Your input is not a xml file or a folder.")
    
###Parse Files###
extension_dict = {"csv" : "dataframe", "json" : "json"}

#Parse if Input is Single File#
if len(content) == 1:
    soup = speechparser.read_protocol(content[0])
    speeches = speechparser.collect_speeches(soup, output = extension_dict[output_extension], 
                                             metadata = args.meta)
    if output_extension == "csv":
        speeches.to_csv(args.output, encoding = "utf-8", index = False)
    elif output_extension == "json":
        with open(args.output, mode = "w", encoding = "utf-8") as f:
            f.writelines(speeches)
    else:
        raise ValueError("Your output format {} is neither 'csv' or 'json'.".format(output_extension))

#Parse if Input is a Folder#
parser_count = 1
conent_len = str(len(content))
if len(content) > 1:
    speeches_list = []
    for file in content:
        print("\rParsing File: {} of {}".format(parser_count, conent_len), end = "")
        parser_count += 1
        soup = speechparser.read_protocol(file)
        speeches_tmp = speechparser.collect_speeches(soup, output = "list", metadata = args.meta)
        speeches_list.extend(speeches_tmp)
    if output_extension == "csv":
        result_df = pd.DataFrame(speeches_list)
        result_df.to_csv(args.output, encoding = "utf-8", index = False)
    elif output_extension == "json":
        with open(args.output, mode = "w", encoding = "utf-8") as f:
            result = json.dumps(speeches_list, ensure_ascii = False, indent = 1)
            f.writelines(result)
    else:
        raise ValueError("Your output format {} is neither 'csv' or 'json'.".format(output_extension))

###Print Success###
print("Speeches written to: {}".format(args.output))