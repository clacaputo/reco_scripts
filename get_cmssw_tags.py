import requests
from bs4 import BeautifulSoup


def get_dpg_pog():
    return ['tracking', 'lumi', 'muon', 'csc', 'rpc', 'gem', 'trk', 'proton', 'dt', 'tau', 'hcal', 'egamma', 'mtd', 'jetmet', 'hgcal', 'ctpps', 'btv', 'ecal', 'pf']

if __name__ == "__main__":
    print(get_dpg_pog())
    for tag in get_dpg_pog():
        URL = "https://github.com/cms-sw/cmssw/issues?q=is%3Aissue+is%3Aopen+label%3A{TAG}+label%3Areconstruction-pending+".format(TAG=tag)     
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
        print(tag.upper(),len(list_issues))
