# pybundestag
Since the 19th plenary period of the German Bundestag, all protocols are published as highly structured xml files. While all former protocols are also available as xml files, there is very little structure  in them, making them nearly equivalent to unstructured txt files.

This Python CLI tool is designed to convert one or more protocols into a single csv or json file. This way, data scientists can use the output for further processing.

### Installation
You will need a copy of Python3 on your computer. There is also the need for two external modules that are not built-in in Python3:
*BeautifulSoup
*Pandas

Make sure that you install those modules. If you want to use pip, you can install them with the following command in your operating system's terminal (e.g. cmd on Windows or Bash on Linux):

```bash
pip install beautifulsoup4 pandas
```

Since pybundestag is hosted only on Github, proceed by downloading this repository (click on 'Clone or download' and then 'ZIP') and unzip it into a destination of your choice.

pybundestag will be published on PyPi so that you can install it via pip.

### Usage
Make sure that you download all the protocols you want to convert as xml files. Keep in mind that you can convert only those documents that were created during or after the 19th plenary period. If you want to convert multiple protocols at once, put them into a single folder.
After you've downloaded all the xml files that you would like to convert, open you operating system's command line terminal and go into where pybundestag resides.

We will invoke pybundestag by using the command line, however it will also need some required arguments:
*-i [--input]: The path of your input file. If you have multiple input files in the same folder, you can just use the folder's path and pybundestag will convert all xml files in it.
*-o [--output]: The path where your result will be written to. This must either be a csv or json file.

pybundestag also supports the following optional arguments:
*-m [--meta]: If present, pybundestag will add meta information to every speech (Date, Location, Plenary Period, and Plenary Session).
*-s [--seperator]: A custom seperator for your csv file (defaults to ","). Make sure that you put qutation marks around your seperator.

Assume that you want to convert a single file in */home/MaxMustermann/rede.xml* and you want to convert it into a csv file under */home/MaxMustermann/output.csv* without meta data and using the default seperator. Also, assume that you are within the pybundestag folder. You can use pybundestag like so:

```bash
python pybundestag.py -i /home/MaxMustermann/rede.xml -o /home/MaxMustermann/output.csv
```

After the script is done, you will get a message that your output was written to the desired path.

If we assume that there are multiple xml files under */home/MaxMustermann/reden/* and you want to convert those files into a single csv file with meta data and a semicolon as a seperator, you can invoke pybundestag like so:

```bash
python pybundestag.py -i /home/MaxMustermann/reden/ -o /home/MaxMustermann/output.csv -m -s ";"
```

You will see the current progress of the program printed to the screen and you will receive a message that your output was written to the desired path. 
Of course, you can change the name of your output file from *output.csv* to *output.json* if you prefer to write to a json file. Note, that your choice of a seperator will be ignored.

All output files will be encoded in UTF-8. 

### Links
You can find all the protocols of the German Bundestag as xml files at the [official website](https://www.bundestag.de/services/opendata).
There is a GitHub organization centered around the German Bundestag called [bundestag](https://github.com/bundestag). There you can find many more repositories for Python and other languages.