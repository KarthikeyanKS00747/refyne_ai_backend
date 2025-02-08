# # test_api.py
# import requests
# import pandas as pd
# import os

# # API base URL
# BASE_URL = "http://localhost:8000"

# def create_sample_csv():
#     """Create a sample CSV file for testing"""
#     data = {
#         'name': ['John', 'Jane', 'Bob'],
#         'age': [25, 30, 35],
#         'city': ['New York', 'London', 'Paris']
#     }
#     df = pd.DataFrame(data)
#     df.to_csv('test_data.csv', index=False)
#     return 'test_data.csv'

# def test_signup():
#     """Test user signup"""
#     url = f"{BASE_URL}/signup"
#     data = {
#         "email": "test@example.com",
#         "password": "testpassword123"
#     }
#     response = requests.post(url, json=data)
#     print("\nSignup Response:", response.status_code)
#     print(response.json())
#     return response.status_code == 200

# def test_login():
#     """Test user login and get token"""
#     url = f"{BASE_URL}/token"
#     data = {
#         "username": "test@example.com",
#         "password": "testpassword123"
#     }
#     response = requests.post(url, data=data)
#     print("\nLogin Response:", response.status_code)
#     print(response.json())
    
#     if response.status_code == 200:
#         return response.json()["access_token"]
#     return None

# def test_file_upload(token):
#     """Test CSV file upload with additional parameters"""
#     url = f"{BASE_URL}/upload-csv"
    
#     # Create test CSV file
#     csv_file = create_sample_csv()
    
#     # Prepare the form data
#     files = {
#         'file': ('alzheimers_prediction_dataset.csv', open('test2/alzheimers_prediction_dataset.csv', 'rb'), 'text/csv')
#     }
#     data = {
#         'string1': 'Hello',
#         'string2': 'World'
#     }
#     headers = {
#         'Authorization': f'Bearer {token}'
#     }
    
#     response = requests.post(url, headers=headers, files=files, data=data)
#     print("\nFile Upload Response:", response.status_code)
#     print(response.json())
    
#     # Clean up the test file
#     os.remove(csv_file)
#     return response.status_code == 200

# def main():
#     print("Starting API tests...")
    
#     # Test signup
#     if not test_signup():
#         print("Signup failed!")
        
    
#     # Test login
#     token = test_login()
#     if not token:
#         print("Login failed!")
#         return
    
#     # Test file upload
#     if not test_file_upload(token):
#         print("File upload failed!")
#         return
    
#     print("\nAll tests completed successfully!")

# if __name__ == "__main__":
#     main()

# import re
# import requests
# from bs4 import BeautifulSoup

# # Given response text
# response_text = '''[text: "- https://www.kaggle.com/datasets/paultimothymooney/cancer-tumor-size-prediction\n- https://data.world/data-collections/breast-cancer-tumor-size\n- https://github.com/omerbsezer/medical-datasets/tree/master/cancer-tumor-size-prediction"
# ]'''

# # Step 1: Extract URLs using regex
# urls = re.findall(r'https?://\S+', response_text)

# # Step 2: Visit and parse each website
# for url in urls:
#     print(f"\nFetching: {url}")
    
#     try:
#         response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#         response.raise_for_status()  # Raise error if request fails

#         # Parse the HTML
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Extract title and first few paragraphs
#         title = soup.title.string if soup.title else "No Title Found"
#         paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")[:3]]  # First 3 paragraphs

#         print(f"Title: {title}")
#         print("First Paragraphs:", paragraphs)

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")

# import requests

# def fetch_kaggle_dataset():
#     url = "https://www.kaggle.com/datasets/ankushpanday1/alzheimers-prediction-dataset-global/download?datasetVersionNumber=1"

#     headers = {
#         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
#         "accept-language": "en-US,en;q=0.9",
#         "priority": "u=0, i",
#         "sec-ch-ua": '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133")',
#         "sec-ch-ua-mobile": "?0",
#         "sec-ch-ua-platform": '"Windows"',
#         "sec-fetch-dest": "document",
#         "sec-fetch-mode": "navigate",
#         "sec-fetch-site": "none",
#         "sec-fetch-user": "?1",
#         "sec-gpc": "1",
#         "upgrade-insecure-requests": "1",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
#     }

#     cookies = {
#         "ka_sessionid": "29cbce99d82dd8dd8b4ae8de6a3b5b46",
#         "GCLB": "CKTYg5-_2o2r8wEQAw",
#         "ACCEPTED_COOKIES": "true",
#         "build-hash": "f67d7966fd2a6401663ba094c99462484cc51c50",
#         "__Host-KAGGLEID": "CfDJ8PHSCL9k9s1HuJ2cRFBFhuiLXK21kftckVXUpBCV5bOo46XAQDccWMh685jiyZ80agl65qYn7-MPiJq5Qqtix3tJnPT_myPuDVyTtULWx5ZytAatt-eC40lK",
#         "CSRF-TOKEN": "CfDJ8PHSCL9k9s1HuJ2cRFBFhuj9FZ7M1Xyg1SKZr6a5xqXI0Lg8WlesKB-QX1akIZQwOUjX584yTh86QQMORtksa04iHRSIY7GzKKB8jgP0bw",
#         "XSRF-TOKEN": "CfDJ8PHSCL9k9s1HuJ2cRFBFhuiZOX9jscx4gzNoATWdgvur0gcqlk0A_MAmW76pK_gmAJmsMjVrzkSCQSWLr7ZKI_ZKOnuUFx1Tohmz7DTsw-aKl2LKu0WtcbXu7BeokNYh40BkRBGTwrpPc-1qHLmWkLE",
#         "CLIENT-TOKEN": "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0..."
#     }

#     try:
#         response = requests.get(url, headers=headers, cookies=cookies, allow_redirects=True)
#         response.raise_for_status()  # Raise an error if request fails

#         # Check if the response contains a redirect to login (meaning authentication is required)
#         if "Sign in" in response.text or response.status_code == 403:
#             print("❌ Authentication required. Please log in to Kaggle and update cookies.")
#             return

#         print("✅ Dataset fetched successfully!")
#         print("Response Headers:", response.headers)
#         print("Response Content (first 500 chars):", response.text)
#         with open("alzheimers_prediction_dataset1.csv", "wb") as file:
#             file.write(response.content)


#     except requests.exceptions.RequestException as e:
#         print(f"❌ Request failed: {e}")

# # Run the function
# fetch_kaggle_dataset()

# import requests
# import csv

# def fetch_and_save_csv():
#     url = "https://www.kaggle.com/datasets/ankushpanday1/alzheimers-prediction-dataset-global/download?datasetVersionNumber=1"

#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
#     }

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Check for errors

#         # Extract data from response (assuming it's in CSV format)
#         lines = response.text.strip().split("\n")  # Split into rows

#         csv_filename = "output.csv"
#         with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)

#             for line in lines:
#                 writer.writerow(line.split(","))  # Split each row by comma

#         print(f"✅ CSV file saved as: {csv_filename}")

#     except requests.exceptions.RequestException as e:
#         print(f"❌ Error fetching data: {e}")

# # Run the function
# fetch_and_save_csv()

# import requests

# # URL
# url = "https://storage.googleapis.com/kaggle-data-sets/6574594/10618775/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20250207%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250207T235345Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=7a55f02e508db5860eafeb8b05ed940181399339929918e8c38e70b317397e1c5ff8d07133f4a49045c0c0d2d33743f4f6ff2fa79f615b9670e698c228f318c3968ac16d5562bdf900c870b7bf69ef94429bf21f8d3661d6a94deeca8e511ddfafef4e5827d6f40306e20ed4851829c2233d8163ea6a3949a1c38e4d7bd7bd08166d4bc15601823353102083cd81be6f96ec0e2d9c241c65095baaaa22034a3502909f81ff1173e3001f62ee7b64ac3bd74cffa757d6ad4018c3ca4b17591cfeba96ff426e48ac6c1719bdfacc82cd396ad0f16cfc083ff7bd4754b5a538163decdb6d11542c7849d2fa1ef49861fa6b9f1975ef3cfd48b89cdbba3a9663cd35"

# # Headers
# headers = {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
#     "accept-language": "en-US,en;q=0.9",
#     "priority": "u=0, i",
#     "sec-ch-ua": '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133")',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Windows"',
#     "sec-fetch-dest": "document",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-site": "none",
#     "sec-fetch-user": "?1",
#     "sec-gpc": "1",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
# }

# # Make the request
# response = requests.get(url, headers=headers, stream=True)

# # Save the file
# if response.status_code == 200:
#     with open("archive.zip", "wb") as file:
#         for chunk in response.iter_content(chunk_size=8192):
#             file.write(chunk)
#     print("✅ File downloaded: archive.zip")
# else:
#     print(f"❌ Error {response.status_code}: {response.reason}")

import os

db_path = "test2\sql_app.db"  # Replace with your database file name

if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✅ Database '{db_path}' deleted successfully.")
else:
    print(f"❌ Database '{db_path}' does not exist.")