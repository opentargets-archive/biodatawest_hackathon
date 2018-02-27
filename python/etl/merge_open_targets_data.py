import sys
import os
import logging
import csv
import requests
from contextlib import closing
from settings import Config

__copyright__ = "Copyright 2014-2018, Open Targets"
__credits__ = ["Gautier Koscielny"]
__license__ = "Apache 2.0"
__version__ = "1.0"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautier.x.koscielny@gsk.com"
__status__ = "Production"

def main():

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    with closing(requests.get(Config.SCORE_FILE_URLS['datasource_scores'], stream=True)) as r:
        #decoded_content = download.content.decode('utf-8')
        reader = csv.reader(r.iter_lines(), delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        c = 0
        for row in reader:
            c += 1
            if c > 1:
                print(row)
            if c > 100:
                break

if __name__ == "__main__":
    main()