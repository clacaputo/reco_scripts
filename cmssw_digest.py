import requests
from bs4 import BeautifulSoup
import re
import os

# Used for dict of lists
from collections import defaultdict
d = defaultdict(list)

def get_dpg_pog():
    return ['tracking', 'lumi', 'muon', 'csc', 'rpc', 'gem', 'trk', 'proton', 'dt', 'tau', 'hcal', 'egamma', 'mtd', 'jetmet', 'hgcal', 'ctpps', 'btv', 'ecal', 'pf']

if len(os.sys.argv) < 2:
    print(f"Missing arguments \nUsage: {os.sys.argv[0]} [CMSSW_Release]")
    exit(-1)

release = os.sys.argv[1]

URL = f"https://github.com/cms-sw/cmssw/releases/{release}"

try:
    page = requests.get(URL)
    page.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
except requests.exceptions.RequestException as e:  # This is the correct syntax
    raise SystemExit(e)

soup = BeautifulSoup(page.content, "html.parser")
list_prs = soup.find("div", class_="markdown-body my-3")

for pr in list_prs.find_all("li"):
    prref  = pr.find("a", class_="issue-link js-issue-link", href=True)
    prnum  = prref.text
    prurl  = prref['href']
    prcodetags = pr.find_all("code")
    prtags = [prt.text for prt in pr.find_all("code")]
    s_prtags = set(prtags)
    s_tags = set(get_dpg_pog())
    #for prt in pr.find_all("code"):
    #    prt.decompose()
    username = re.compile("\@\w[^:]+") # [^:]+ select all the symbols until the first : occurence

    if 'reconstruction' in prtags:
        #print(prnum)
        #print(prurl)
        #print(prtitle)
        #print(prtags)
        #print("--"*20)
        #print(pr.text)
        splittingPoint = username.findall(pr.text)[0]
        prtitle = pr.text.split(splittingPoint)[-1][2:]
        #print(username.findall(pr.text))
        print(f"{prtitle} [[{prurl}][(#{prnum[1:]})]]")
        intersaction = s_tags.intersection(s_prtags)
        if intersaction:
            d[intersaction.pop()].append(f"{prtitle} [[{prurl}][(#{prnum[1:]})]]")
        else:
            d["general"].append(f"{prtitle} [[{prurl}][(#{prnum[1:]})]]")
        #for tag in get_dpg_pog():
        #    if tag in prtags:
        #        d[tag].append(f"{prtitle} [[{prurl}][(#{prnum[1:]})]]")
        #    else:
        #        d["general"].append(f"{prtitle} [[{prurl}][(#{prnum[1:]})]]")
    #for prt in prtags:
     #   print(prt, prt.text, prt.text.format("utf-8"))

for k in d.keys():
    print(f"   * *{k}*: ", ", ".join(d[k]))
