import os
import boto3
#from dotenv import load_dotenv, find_dotenv

#load_dotenv(find_dotenv())

#dotenv_path = os.path.join(os.path.dirname(__file__), ".env-sample")
#load_dotenv(dotenv_path)

username = "STAGING_Jmharri@harri.com"
password = "House123!"

client = boto3.client("cognito-idp", region_name="us-east-1")

print(os.getenv("6hvg0o3ht23isvn67giahhbgee"))

# Initiating the Authentication, 
response = client.initiate_auth(
    ClientId="6hvg0o3ht23isvn67giahhbgee",
    AuthFlow="USER_PASSWORD_AUTH",
    AuthParameters={"USERNAME": username, "PASSWORD": password},
)

# From the JSON response you are accessing the AccessToken
print(response)
# Getting the user details.
access_token = response["AuthenticationResult"]["AccessToken"]

response = client.get_user(AccessToken=access_token)
print(response)