import os
import requests
import numpy as np

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt 

if len(os.sys.argv) != 2:
    print(f"Missing arguments \nUsage: {os.sys.argv[0]} date [yyyy-mm-dd] ")
    exit(-1)

SDATE = os.sys.argv[1]

def get_dpg_pog():
    return ['tracking', 'lumi', 'muon', 'csc', 'rpc', 'gem', 'trk', 'proton', 'dt', 'tau', 'hcal', 'egamma', 'mtd', 'jetmet', 'hgcal', 'ctpps', 'btv', 'ecal', 'pf']

if __name__ == "__main__":
    x_list = []
    y_list = []
    for_hist = []
    print(get_dpg_pog())
    for i, tag in enumerate(get_dpg_pog()):
        URL = "https://github.com/cms-sw/cmssw/issues?q=is%3Apr+is%3Aclosed+label%3A{TAG}+label%3Areconstruction-approved+".format(TAG=tag)     
        try:
            page = requests.get(URL)
            page.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        soup = BeautifulSoup(page.content, "html.parser")
        list_issues_container = soup.find("div", class_="js-navigation-container")
        if list_issues_container is None:
            print(tag.upper(),0)
            continue
        list_issues = list_issues_container.find_all("div", class_="flex-auto")
        x_list.append(tag.upper())
        y_list.append(len(list_issues))
        for i in range(0,len(list_issues)):
            for_hist.append(i)
        print(tag.upper(),len(list_issues))
    
    x_values = np.arange(0, len(x_list)+1)
    new_x = np.sort(np.concatenate((x_values[1:]-0.2,x_values[1:]+0.2) )) 
    new_y = np.repeat(y_list,3)
    mask = np.tile([True, True, False], 9)
    #plt.fill_between(new_x, new_y, 0 , where=mask)
    plt.hist(for_hist, bins=np.linspace(0,15,16))
    plt.savefig("stat_pr.png")
