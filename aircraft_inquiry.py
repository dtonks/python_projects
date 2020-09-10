import pandas as pd
import requests
import csv
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def get_data(tail_number):
  html = f"https://registry.faa.gov/aircraftinquiry/NNum_Results.aspx?NNumbertxt={tail_number}"
  page = requests.get(html)
  soup = BeautifulSoup(page.content, 'html.parser')

  try:
    data = { 'ID': "",
             'CustID': "",
             'Customer': "",
             'AircraftYear': soup.find(id="ctl00_content_Label17").get_text(),
             'AircraftMakeModel': (soup.find(id="ctl00_content_lbMfrName").get_text()).strip()+ " " + (soup.find(id="ctl00_content_Label7").get_text()).strip(),
             'AircraftType': "HELICOPTER" if soup.find(id="ctl00_content_Label11").get_text().strip().upper() == 'ROTORCRAFT' else soup.find(id="ctl00_content_Label11").get_text().strip().upper(),
             'TailNumber': tail_number,
             'RegisteredName': soup.find(id="ctl00_content_lbOwnerName").get_text().strip().upper(),
             'RegistrationExpires': soup.find(id="ctl00_content_Label9").get_text().strip(),
             'Project': "",
             'ProjectPlan': "",
             'Notes': "",
             'BasedAircraft': "",
             'DeRegistered': "",
             'Active': "",
            }
  except AttributeError:
    data = { 'ID': "",
             'CustID': "",
             'Customer': "",
             'AircraftYear': "*ERROR - RECORD MANUALLY*",
             'AircraftMakeModel': "*ERROR - RECORD MANUALLY*",
             'AircraftType': "*ERROR - RECORD MANUALLY*",
             'TailNumber': tail_number,
             'RegisteredName': "*ERROR - RECORD MANUALLY*",
             'RegistrationExpires': "*ERROR - RECORD MANUALLY*",
             'Project': "",
             'ProjectPlan': "",
             'Notes': "",
             'BasedAircraft': "",
             'DeRegistered': "",
             'Active': "",
            }

  return data

def results_csv(tail_numbers):
  fieldnames = ['ID','CustID','Customer','AircraftYear','AircraftMakeModel','AircraftType','TailNumber','RegisteredName','RegistrationExpires','Project','ProjectPlan','Notes','BasedAircraft','DeRegistered','Active']
  with open("results.csv", 'w') as file:
    writer = csv.DictWriter(file, fieldnames = fieldnames)
    writer.writeheader()
    for tail_number in tail_numbers:
      writer.writerow(get_data(tail_number))

# t = ['N223MK', 'N228DF', 'N846U', 'N31617', 'N942WG']
# t = ['N6517A']

# results_csv(['N223MK', 'N228DF', 'N846U', 'N31617', 'N942WG'])

def create_list(filename):
  df = pd.read_excel(filename) # can also index sheet by name or fetch all sheets
  mylist = df['TailNumber'].tolist()
  return mylist
print("create .xlsx file listing the tailnumbers with the column header as 'TailNumber'")
print("Put .xlsx file location as script")
print("input file name (example.xlsx): ")
filename = input(str(""))
print(f"Collecting data for {len(create_list(filename))} tailnumbers: {create_list(filename)}")

results_csv(create_list(filename))

# Can also manually enter list
# results_csv(['N6517A', 'N657PP', 'N5495C', 'N454DM', 'N315CK', 'N271SM', 'N272SM', 'N273SM', 'N274SM', 'N2149C', 'N7327E', 'N90333', 'N3001B'])


'''
Old dictionary:

    data = {}
    data['ID'] = ""
    data['CustID'] = ""
    data['Customer'] = ""
    data['AircraftYear'] = soup.find(id="ctl00_content_Label17").get_text()
    data['AircraftMakeModel'] = (soup.find(id="ctl00_content_lbMfrName").get_text()).strip()+ " " + (soup.find(id="ctl00_content_Label7").get_text()).strip()
    data['AircraftType'] = soup.find(id="ctl00_content_Label11").get_text().strip()
    data['TailNumber'] = tail_number
    data['RegisteredName'] = soup.find(id="ctl00_content_lbOwnerName").get_text().strip()
    data['RegistrationExpires'] = soup.find(id="ctl00_content_Label9").get_text().strip()
    data['Project'] = ""
    data['ProjectPlan'] = ""
    data['Notes'] = ""
    data['BasedAircraft'] = ""
    data['DeRegistered'] = ""
    data['Active'] = ""
'''

'''
Code below is trying to account for the webpages that require you to click 'continue' link
1. check to see if i cant retrieve data from original path
2. except AttributeError it causes
3. import js2py
4. write javascript to move to window
5. javascript to click contiue utton
6. try to set the new page as the next page after clicking continue
7. Errors recieved because the url stays the same so I continue to use the same url
8. Possible solutions: try to get the aircraft registration database
                       https://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download/
Code:
import js2py
  try:
    data['AircraftYear'] = soup.find(id="ctl00_content_Label17").get_text()
  except AttributeError:
    move = "function move(){window.location = html};"
    click_continue = "function click_continue(){document.getElementById('ctl00_content_lbtnWarning').click(); window.location.href;}"
    js2py.eval_js(move)
    js2py.eval_js(click_continue)
    page2 = page.eval_js(click_continue)
    soup = BeautifulSoup(page2.content, 'html.parser')
'''
