# pybundestag
Since the 19th plenary period of the German Bundestag, all protocols are published as highly structured xml files. While all former protocols are also available as xml files, there is very little structure in them, making them nearly equivalent to unstructured txt files. 

Also, the Bundestag publishes information on all current and former members (MdB) in a highly structured XML file, containing personal information, a short CV, and period specific infos.

This Python CLI tool is designed to convert protocols and the file on all MdBs into single csv or json files. This way, data scientists can use the output for further processing.

### Installation
You will need a copy of Python3 on your computer. There is also the need for two external modules that are not built-in in Python3:
*BeautifulSoup
*Pandas

Make sure that you install those modules. If you want to use pip, you can install them with the following command in your operating system's terminal (e.g. cmd on Windows or Bash on Linux):

```bash
pip install beautifulsoup4 pandas
```

Since pybundestag is hosted only on Github, proceed by downloading this repository (click on 'Clone or download' and then 'ZIP') and unzip it into a destination of your choice.

pybundestag will be published on PyPi soon so that you can install it via pip.

### Usage

You can use a consistent syntax  within pybundestag for converting both protocols and the MdB XML file. The general syntax is like this:

```bash
python bundestag.py entity input output
```

entity can either be 'protocol' or 'mdb', depending on the task at hand. If you want to parse protocols, choose 'protocol'. If you want to convert the MdB XML file, use 'mdb'. 'input' should be the path of your protocol(s) or MdB XML file while output is the desired path of your output. When parsing Bundestag protocols, you can also specify a folder and pybundestag will parse all XML files in that folder. Both 'protocol' and 'mdb' support several optional arguments.

#### Parsing of Protcols
Make sure that you download all the protocols as XML files you want to convert. Keep in mind that you can convert only those documents that were created during or after the 19th parliamentary period. If you want to convert multiple protocols at once, put them into a single folder.
After you've downloaded all the XML files that you would like to convert, open you operating system's command line tool and go into where pybundestag resides.

You can use the CLI interface as discussed above. However, you can also use the following optional arguments:
* -m [--meta]: If present, pybundestag will add meta information to every speech (Date, Location, Plenary Period, and Plenary Session).
* -s [--seperator]: A custom seperator for your csv file (defaults to ","). Make sure that you put quotation marks around your seperator.

Assume that you want to convert a single file in */home/MaxMustermann/rede.xml* and you want to convert it into a csv file under */home/MaxMustermann/output.csv* without meta data and using the default seperator. Also, assume that you are within the pybundestag folder. You can use pybundestag like so:

```bash
python pybundestag.py protocol /home/MaxMustermann/rede.xml /home/MaxMustermann/output.csv
```

After the script is done, you will get a message that your output was written to the desired path.

If we assume that there are multiple XML files under */home/MaxMustermann/reden/* and you want to convert those files into a single csv file with meta data and a semicolon as a seperator, you can invoke pybundestag like so:

```bash
python pybundestag.py protocol /home/MaxMustermann/reden/ /home/MaxMustermann/output.csv -m -s ";"
```

You will see the current progress of the program printed to the screen and you will receive a message that your output was written to the desired path. The resulting csv file will contain the speeche's unique Id, Date, Faction of speaker, Location, Parliamentary Period, Role of Speaker, Session, Name of Speaker, ID of Speaker, and the raw text (stripped of comments).

Of course, you can change the name of your output file from *output.csv* to *output.json* if you prefer to write to a json file. Note, that your choice of a seperator will be ignored then.

#### Parsing MdB XML
If you would like to convert the XML file containing information on all MdBs, you can use 'mdb' as the first postional argument to pybundestag. The input must be a XML file as provided by the Bundestag. Just as you would do when converting protocols, specify your output as either a csv or json file. 

There are also some optional arguments you can use:
* -p [--period]: You can specify a certain parliamentary period. pybundestag will only convert and export members of that parliamentary period and add information specific to that period (e.g. type of mandate and electoral district). This should be an integer.
* -i [--institutions]: Here you can insert multiple institution names (e.g. committees or factions). pybundestag will check if the MdB was also a member of that institution. If there is more than one institution to check, you must seperate them by using a ";". Note that you must also specify a period if you use this option. In your final result, you will get a boolean variable for every institution you put in. True will imply that the MdB was part of that institution during the period specified. False would imply otherwise. There is no sanity check, so make sure that your spelling is correct.

If you simply want to convert all MdBs in */home/MaxMustermann/mdbs.xml* to */home/MaxMustermann/mdbs.csv*, you would use pybundestag like so:
```bash
python pybundestag.py mdb /home/MaxMustermann/mdbs.xml /home/MaxMustermann/mdbs.csv
```

This will yield a csv file containing personal information (e.g. name, and date of birth, gender, etc.) as well as a short cv and a unique ID.

A more complex example would be if you want to extract all MdBs of the 19th parliamentary period to a json file, while also checking if a given MdB was member of the 'Verteidigungsausschuss' and/or  'Ausschuss für Arbeit und Soziales':

```Bash
python pybundestag.py mdb /home/MaxMustermann/mdbs.xml /home/MaxMustermann/mdbs.json -p 19 -i "Verteidigungsausschuss;Ausschuss für Arbeit und Soziales"
```

This file will not only contain personal information, a unique ID, and a short CV but also period specific information and two dummy variables 'member_Verteidigungsausschuss' and 'member_Ausschuss für Arbeit und Soziales'.

### Links
You can find all the protocols of the German Bundestag and data on all MdBs (former and current) as XML files at the [official website](https://www.bundestag.de/services/opendata).
There is a GitHub organization centered around the German Bundestag called [bundestag](https://github.com/bundestag). There you can find many more repositories for Python and other languages.