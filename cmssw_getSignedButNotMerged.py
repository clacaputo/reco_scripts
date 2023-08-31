import requests
from bs4 import BeautifulSoup
import re
import os
from collections import defaultdict

if len(os.sys.argv) < 3:
    print(f"Missing arguments \nUsage: {os.sys.argv[0]} [CMSSW_Release_Milestone] [yyyy-mm-dd] [true|false]")
    exit(-1)

MILESTONE = os.sys.argv[1]
DATE = os.sys.argv[2]
pending = os.sys.argv[3]

if "CMSSW" not in MILESTONE:
    print(f"MILESTON format must be: CMSSW_A_B_X, where A and B are choosen by you \n You provided: {MILESTONE}")
    exit(-1)

URL = f"https://github.com/cms-sw/cmssw/pulls?q=is%3Apr+milestone%3A{MILESTONE}+label%3Areconstruction-approved+updated%3A%3E{DATE}+is%3Aopen+"

if pending.upper() == "TRUE":
    URL = f"https://github.com/cms-sw/cmssw/pulls?q=is%3Apr+milestone%3A{MILESTONE}+label%3Areconstruction-pending+is%3Aopen"

try:
    print(URL)
    page = requests.get(URL)
    page.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
except requests.exceptions.RequestException as e:  # This is the correct syntax
    raise SystemExit(e)

soup = BeautifulSoup(page.content, "html.parser")
list_prs = soup.find("div", class_="js-navigation-container")

count = 0
pr_type_dict = defaultdict(list)
for pr in list_prs.find_all("div", class_="flex-auto"):
    count+=1
    prref  = pr.find("a", class_="Link--primary", href=True)
    tag = pr.find("a", class_="IssueLabel", attrs={'style':"--label-r:37;--label-g:127;--label-b:219;--label-h:210;--label-s:71;--label-l:50;"})
    prtitle  = prref.text
    prurl  = prref['href']
    fulltext = "{title} (#{pr})".format(title=prtitle, pr=prurl.split('/')[-1] )
    if tag is None:
        #print(count, fulltext, tag)
        pr_type_dict["general"].append(fulltext)
    else:
        tag = tag.text.strip()
        pr_type_dict[tag].append(fulltext)
       # print(count, fulltext, tag)


for k, i in pr_type_dict.items():
    str_of_prs = "".join( f"{x}, " for x in i)
    print(f"{k.upper()}: {str_of_prs}")


ccWed12142207#
ccFermilab22