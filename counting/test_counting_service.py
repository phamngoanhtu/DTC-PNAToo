import json
import requests


counting_url = 'http://0.0.0.0:5004/counting'

headers = {'Content-type': 'application/json'}
data = {
    'vehicle_trajectory':
            (
                [1,2,3,4],
                [4,5,6,7],
            ),
    'video_id':10
}
response = requests.post(counting_url, json=data, headers=headers)
print(response)