from pocket import Pocket

# Set up Pocket API credentials
consumer_key = input("your consumer key: ")
redirect_uri = "https://getpocket.com/de/home"
pocket_instance = Pocket(consumer_key, access_token=None)

# Obtain a request token
request_token = pocket_instance.get_request_token(redirect_uri=redirect_uri, consumer_key=consumer_key)
auth_url = Pocket.get_auth_url(code=request_token, redirect_uri=redirect_uri)
print(auth_url)
input("Finished?(press enter)")
user_credentials = Pocket.get_credentials(consumer_key=consumer_key, code=request_token)
access_token = user_credentials['access_token']
print(f"Your access token: {access_token}")