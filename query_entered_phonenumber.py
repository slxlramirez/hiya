import requests
import base64
import csv
from csv import DictReader
import os
from datetime import datetime

def build_creds():
    _filename = ''
    global _env 
    
    tmp = int(input("Which environment do you want to query?\nEnter 1 for Prod\nor 2 for Test:"))
    _env = tmp
    
    if _env == 1:
        _filename = 'csv_files/credentials/credentials_prod.csv'
    elif _env == 2:
        _filename = 'csv_files/credentials/credentials_test.csv'
    else:
        print(f'Sorry {_env} if not a supported entry.')
        quit()
    
    with open(_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=':')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                app_id = row[0]
                app_secret = row[1]
                encoded_appsecret = base64.b64encode((app_id + ':' + app_secret).encode()).decode()
                return (encoded_appsecret)
            else:
                print("Why did this run?")
                # this should not run bc the file should only have 1 row in it!

def build_url(cc,number):
    return base_url + cc + '/' + number

def query_hiya(url):
    global getResponse 
    getResponse = requests.get(url, headers=headers)
    if getResponse.status_code == 200:
        res = getResponse.json()
        print(res)
    else:
        print(url + ":" + str(getResponse.status_code))
    return getResponse.status_code

def update_hiya(url, cc, number):
    print('Entered Update...')
    
    _num = cc + '/' + number
    print(f'We will query {url}')
    print(f'Using {_num}')   
    jsonValues = parse_response()
    #print('jsonValues is currently:\n')
    #print(jsonValues)
    

    jsonPayload = createJsonPayload(jsonValues)
    print('Verifying return worked ok.\njsonPayload is currently:\n')
    print(jsonPayload)
    
    proceed = input("Do you want to attempt the PUT request with that payload?: (y or n)")
    if proceed == 'y':
        print('Proceeding to the PUT request rn...\n')
        response = requests.put(url, json=jsonPayload, headers=headers)
        print("Response code: " + str(response.status_code))
        print("This is the JSON response: \n")
        print(response.json())
    else:
        print("Standing down...")
    
    #data = parse_response()
    #print(f'Data is:\n{data}')

def createJsonPayload(jsonValues):
    data = {"doNotOriginate": False, "display": {"displayName": "", "logoId": "", "callReason": "", "country": "", "state": "",  "city": "", "
managedBrand": ""}, "secureCall": {"activate": False, "failureRouting": ""}}
    print("Data came in as:\n")
    print(data)
    data["doNotOriginate"] = jsonValues[0]
    data["display"]["displayName"] = jsonValues[1]
    data["display"]["logoId"] = jsonValues[2]
    data["display"]["callReason"] = jsonValues[3]
    data["display"]["country"] = jsonValues[4]
    data["display"]["state"] = jsonValues[5]
    data["display"]["city"] = jsonValues[6]
    data["display"]["managedBrand"] = jsonValues[7]
    data["secureCall"]["activate"] = jsonValues[8]
    data["secureCall"]["failureRouting"] = jsonValues[9]
    
    print("Data is now:\n")
    print(data)
    return(data)
    
def parse_response():
    res = getResponse.json()
    print(f'res is currently\n{res}')
    
    values = []
    doNotOriginate = ''
    displayName = ''
    logoId = ''
    callReason = ''
    country = ''
    state = ''
    city = ''
    managedBrand = ''
    activate = input("Set activate to True or False?: ")
    failureRouting = 'WARN'
    
    print(f'Res Display Active is {res["display"]["active"]}')
    print(f'Res Display Pending is {res["display"]["pending"]}')
    
    if res['display']['active']:
        print("ACTIVE HAS DATA\n")
        doNotOriginate = res["doNotOriginate"]
        displayName = res["display"]["active"]["displayName"]
        logoId = res["display"]["active"]["logoId"]
        callReason = res["display"]["active"]["callReason"]
        country = res["display"]["active"]["country"]
        state = res["display"]["active"]["state"]
        city = res["display"]["active"]["city"]
        managedBrand = res["display"]["active"]["managedBrand"]
    else:
        print("ACTIVE does NOT have data...rip\n")
    values.extend([doNotOriginate,\
        displayName,\
        logoId,\
        callReason,\
        country,\
        state,\
        city,\
        managedBrand,\
        activate,\
        failureRouting
        #res["secureCall"]["active"],\
        #res["secureCall"]["failureRouting"]\
        ])
    #print('Values is:\n')
    #print(values)
    return(values)

def main():
    print("Starting...")
    global base_url
    global encoded_appsecret
    global headers
    global current_status_csv
    global updated_status_csv
    global error_log_csv
    global syslog_server
    global syslog_port
    global _env
    global getResponse
    
    base_url = 'https://connect.api.hiyaapi.com/v1/phone/'
    encoded_appsecret = build_creds()
    headers = {"Authorization": "Basic %s" % encoded_appsecret}
    current_status_csv = 'csv_files/current_status.csv'
    updated_status_csv = 'csv_files/updated_status.csv'
    error_log_csv = 'csv_files/errors.csv'
    syslog_server = '172.19.19.19'
    syslog_port = '1514'
    
    cc = input("Which CC? ")
    number = input("Which number? ")
    url = build_url(cc,number) 
    proceed = query_hiya(url)
    if proceed == 200:
        print("response code was 200 (this is good)")
        update_hiya(url, cc, number)
        #update_hiya(url,row[0],row[1],row[2],row[3])
    print("Finished...")
                
if __name__=="__main__":
    main()
