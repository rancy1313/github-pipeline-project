# handle requests 
import requests 

# rest after each call (rate management/for sanity)
import time

# get data with endpoint and headers
def get_data(endpoint, headers):

    try:
        # get data using endpoint
        url = "https://api.github.com" + endpoint
        r = requests.get(url, headers=headers)
    
        # rest 0.5
        time.sleep(0.5)
    
        # (repo commit endpoint error)
        # if 409 status code then commit history not accessible
        # or 451 means the resource is unavailable for legal reasons
        # 404 not found
        # so do nothing
        if r.status_code in [404, 409, 451]:
            return []
        # check for other errors 
        else:
            r.raise_for_status()
    
            # return json data
            return r.json()

    # handle HTTP status errors first, then catch other request failures
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
        
    except requests.exceptions.RequestException as e:
        print("Other request error:", e)