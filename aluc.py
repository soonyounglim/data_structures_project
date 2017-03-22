#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
# Anthony Luc
# NetID: aluc
# Adapted from: https://github.com/benhoff/facebook_api_script/blob/master/get_facebook_pictures.py

import json
import os
import urllib.request

def return_data(url, api_key):
    request = urllib.request.Request(url)
    request.add_header('Authorization', 'Bearer {}'.format(api_key))

    response = urllib.request.urlopen(request)
    encoding = response.headers.get_content_charset()

    data = json.loads(response.read().decode(encoding))
    
    return data 


def main():
    print("Entered Main")

    base_url = "https://graph.facebook.com/v2.8/"

    #TODO: find FB API Key
    facebook_api_key = os.getenv('FACEBOOK_API_KEY')

    print("KEY: %s" % facebook_api_key)

    # This is getting out the user id!
    data = return_data(base_url+"me", facebook_api_key)
    # Will need id for parsing photo tags
    user_id = data['id']

    # This is getting out the data for favourite teams.
    data = return_data(base_url+"me?fields=favorite_teams", facebook_api_key)

    data = data['name']
    print(data)


if __name__ == '__main__':
    main()