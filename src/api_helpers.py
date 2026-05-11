# handle requests 
import requests 

# get data with endpoint and headers
def get_data(endpoint, headers):

    # get data using endpoint
    url = "https://api.github.com" + endpoint
    r = requests.get(url, headers=headers)

    # (repo commit endpoint error)
    # if 409 status code then commit history not accessible
    # so do nothing
    if r.status_code == 409:
        return []
    # check for other errors 
    else:
        r.raise_for_status()

        # return json data
        return r.json()