import requests

def req_test():
    # URL for the GET

    access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzMTg5MTI0LCJpYXQiOjE2OTMxODE5MjQsImp0aSI6ImNkODQ5MDM1NzJhYTRmNzM5YzM3MmE0YzA1YzhiNTkzIiwidXNlcl9pZCI6Mn0.KodRdXAarRXTmFpiZYQ_10XU0lz_QqHYgiwTd-pxteg'
    url = "http://127.0.0.1:8000/exercises/admin/"
    headers = {"Authorization": f"Bearer {access_token}"}

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Process the response
    if response.status_code == 200:
        response = response.json()
        return response
    else:
        response_data = response.json()
        response_message = response_data['Message']
        return response_message


if __name__ == "__main__":
    print(req_test())