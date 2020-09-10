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

results_csv(['N223MK', 'N228DF', 'N846U', 'N31617'])
