import requests

def req_test():
    try:
        url = "http://127.0.0.1:8000/auth/login/"
        payload = {
            "username": "admin",
            "password": "admin123"
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        return data["tokens"]["access"]
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


if __name__ == "__main__":
    print(req_test())