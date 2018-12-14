#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import requests
import os, sys
from zipfile import ZipFile
from urllib.error import URLError, HTTPError, ContentTooShortError

RED = '\x1b[91m'
RED1 = '\033[31m'
BLUE = '\033[94m'
GREEN = '\033[32m'
BOLD = '\033[1m'
NORMAL = '\033[0m'
ENDC = '\033[0m'

def file_download():
    zip_file_url = "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip"
    print(GREEN + 'Downloading: {0}'.format(zip_file_url) + ENDC)
    try:
        r = requests.get(zip_file_url, stream=True)
        if r.status_code != 200:
            print(RED + " * Error: Could not complete the download of the new version. Check your internet connection." + ENDC)
            return False
        with open('D_megase.zip', 'wb') as f:
            f.write(r.content)

        z = ZipFile('D_megase.zip', 'r')
        print(GREEN + " * Extracting new version..." +ENDC)
        z.extractall(path='./data/')
        z.close()
        os.remove('D_megase.zip')
        print(GREEN + " * Replacing the current file with the new file..."  + ENDC)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print(RED + " * Error: Download error: ",e.reason + ENDC)


def download(url, user_agent='wswp', num_retries=2):
    print('Downloading: {0} - Attempt: {1}'.format(url, (num_retries - num_retries) + 1))
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        html = urllib.request.urlopen(url).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error: ',e.reason)
        html = None
        if (num_retries > 0):
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html

# url = "http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip"
# html = download(url,3)
# if (html != None):
#     print(html)

file_download()