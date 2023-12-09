import requests
import random

def make_api_request( bearer_token):
    url = "http://127.0.0.1:8000/submission/43e67/runrccode/"
    
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "question": "1f91a",
        "input": "hello",
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        
        if response.status_code == 200:
            print("++++++++++++")
        else:
            print("API request failed with status code:", response.status_code)
    except Exception as e:
        print("Error occurred during API request:", str(e))


# Example usage:
bearer_token = ["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3NzQ0NjM1LCJpYXQiOjE2OTc3MzM4MzUsImp0aSI6IjI2NDU3NzU5YTAxYzRkNTNhMmMwYTZmMmJiMjQ2ZTAwIiwidXNlcl9pZCI6MX0.B-MT7dG-i6Q9v4t6mLNtXVSQA8bEqWRNQlFsIjTp0kA","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3NzQ3NDM2LCJpYXQiOjE2OTc3MzY2MzYsImp0aSI6Ijg3OGM2ZmRkNjY1ZDRiNjViZmFlMzZkNmQ0MGJhM2Q5IiwidXNlcl9pZCI6Mn0.pBkNELNdPo1UTovhcNLI0mkoPlRaOBHHqe0CPHKhNgY","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3NzQ3NDU2LCJpYXQiOjE2OTc3MzY2NTYsImp0aSI6ImU2YWQyZTQyOTBiNzQ0MTdhYjdiZDJlZjRlYjNmMGFkIiwidXNlcl9pZCI6M30.-FYyWMGg1pWLCpy-O_FUNnBgqS-3bGdQq-OoXZ7I1gs","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3NzQ3NDY3LCJpYXQiOjE2OTc3MzY2NjcsImp0aSI6ImJhNzQyZWJlNWZhYTQyMzViMWQwZmU4YTFmMDI4MDQ2IiwidXNlcl9pZCI6NH0.8-Vndnq_qoSHPFQblZ0KgFQLnI6vQLxJUZ84xWNtLsg","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3NzQ3NDgwLCJpYXQiOjE2OTc3MzY2ODAsImp0aSI6IjVkOTAzOWI5YTA0ODQ4MWQ4NDBlYTdkOWEwN2RiMTY3IiwidXNlcl9pZCI6NX0.3g9enRdNKLwM-in0gBPj8fGSA7ods0C3dmhUvRbdfu0","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3NzQ3NDkyLCJpYXQiOjE2OTc3MzY2OTIsImp0aSI6IjAzNmRmMGY1ZTI3MzRmNzBiMDExMjU0NWFkODg2ZTBlIiwidXNlcl9pZCI6Nn0.FE1sKLAfbtI2AvFbybLstj3V-yALOPVDcoyMOS5pXe0"]

for i in range(300):
    x = random.randint(0, 5)
    print("user : ",x)
    response = make_api_request( bearer_token[x])
