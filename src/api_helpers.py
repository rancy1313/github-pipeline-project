# handle requests 
import requests 

# rest after each call (rate management/for sanity)
import time

# used to count api calls
api_call_counter = 0

# get data with endpoint and headers
def get_data(endpoint, headers):

    # use global var
    global api_call_counter
    # increment at each call
    api_call_counter += 1

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

# helper to print the api call count
# saves current count, prints it, and then resets global
# pass current count to keep track of total for whole notebook
def print_api_call_count():

    global api_call_counter

    current_count = api_call_counter

    print(f"Total API calls: {current_count}")

    # reset counter
    api_call_counter = 0

    return current_count