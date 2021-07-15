import requests
import json

#server
BASE = 'http://127.0.0.1:8080/'

data = [{'event': 'school', 'date': '2021-07-17'},
        {'event': 'beach', 'date': '2021-07-20'},
        {'event': 'dinner', 'date': '2021-07-15'},
        {'event': 'lunch', 'date': '2021-07-15'}]

#response = requests.post(BASE + 'event', data)

#for i in range(len(data)):
#    response = requests.post(BASE + "event", data[i])
#    print(response.json())

r = requests.get(BASE + 'event')
print(r.json())

#start time and end time functionality test
dates = {'start_time': '2021-07-16', 'end_time': '2021-07-19'}
response = requests.get(BASE + 'event', params=dates)
print(response.json())


today_response = requests.get(BASE + "event/today")
print(today_response.json())
