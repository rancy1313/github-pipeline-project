# dict flattening functions
from src.flattening_data import (
    flatten_repo_dictionaries,
    flatten_repo_commit_dictionaries,
    flatten_repo_issues_dictionaries,
    normalize_data_columns
)

# get data from GitHub REST API
from src.api_helpers import (
    get_data
)

# main pipeline to ingest more users/repos/commits/issues
def run_pipeline(headers, rename_users_map, rename_repos_map, rename_commits_map, rename_issues_map, most_recent_user_id):

    # pipeline vars

    # number of pages to ingest
    pages = 3

    # pagination size
    users_per_page = 20
    repos_per_page = 10
    commits_per_page = 20
    issues_per_page = 20
    
    # store user/repos/commits/issues data
    all_users_data = []
    all_repos_data = []
    all_commits_data = []
    all_issues_data = []

    # for each page get x users
    for i in range(pages):

        # get users data
        endpoint = f"/users?since={most_recent_user_id}&per_page={users_per_page}"

        # returns list
        users = get_data(endpoint, headers)

        # break if users is empty list > stop pagination loop
        if not users:
            break

        # get the usernames to get more data
        logins = [user["login"] for user in users]

        # for each user get more detailed data
        for login in logins:
            
            # endpoint for specific user data using username
            endpoint = f"/users/{login}"

            # returns a dict per user
            user_data = get_data(endpoint, headers)

            # rename user data cols
            normalize_data_columns(user_data, rename_users_map)

            # append user dict to all data
            all_users_data.append(user_data)

            # repo section
            
            # endpoint for specific user repos data using username
            endpoint = f"/users/{login}/repos?per_page={repos_per_page}"

            # returns a list
            repo_data = get_data(endpoint, headers)
            
            # for each repo get the commits/issues for that repo
            for repo in repo_data:

                # flatten repo dictionaries
                flatten_repo_dictionaries(repo)

                # get repo name for url
                repo_name = repo["name"]

                # get repo id for flattening commits/issues dicts
                repo_id = repo['id']

                # rename repo data cols
                normalize_data_columns(repo, rename_repos_map)

                # endpoint for getting commits of a user's specific repo
                endpoint = f"/repos/{login}/{repo_name}/commits?per_page={commits_per_page}"

                # returns a list
                commit_data = get_data(endpoint, headers)

                # flatten the dictionaries in each commit
                for row in commit_data:
            
                    flatten_repo_commit_dictionaries(row, repo_id)

                    # rename commits data cols
                    normalize_data_columns(row, rename_commits_map)

                all_commits_data.extend(commit_data)

                # this section is to ingest issues data
                
                # if repo has issues then call
                if repo["has_issues"] == True:
                    
                    # # endpoint for getting issues of a user's specific repo
                    endpoint = f"/repos/{login}/{repo_name}/issues?per_page={issues_per_page}"

                    # returns list
                    issue_data = get_data(endpoint, headers)

                    # flatten the dictionaries in each issue 
                    for row in issue_data:
                        
                        flatten_repo_issues_dictionaries(row, repo_id)

                        # rename commits data cols
                        normalize_data_columns(row, rename_issues_map)
    
                    # add issue data to all issues data
                    all_issues_data.extend(issue_data)

            # extend repos data list to include repo data
            all_repos_data.extend(repo_data)
        
        # GitHub REST api with users endpoint uses 'since' to get the users where the id is after 'most_recent_user_id'
        # therefore, get the last id of the current call to get the next page
        most_recent_user_id = users[-1]["id"]

    # return data to insert in the DB staging tables
    return all_users_data, all_repos_data, all_commits_data, all_issues_data

# function to ingest more repos/commits/issues for existing users
# num number of repos
# commits/issues ingested matches max length for existing repos to ensure consistent sizes
# **kwargs for unused vars
def get_repos_data(num, conn, headers, rename_repos_map, rename_commits_map, rename_issues_map, **kwargs):

    # init lists to store data
    repos_data = []
    commits_data = []
    issues_data = []

    # pagination sizes
    repo_page_size = 20
    
    # commits/issues pagination sizes uses the max number for each repo bc it is less than
    # the pagination max per call

    # set max pages to search through (safety exit)
    max_pages = 5

    # fetch list of users in the DB
    cur = conn.cursor()

    sql_query = """
        SELECT
            login
        FROM users
    """

    cur.execute(sql_query)

    logins = cur.fetchall()

    # flatten
    logins = [login[0] for login in logins]

    # get lsit of existing repo ids in DB
    sql_query = """
        SELECT
            repo_id
        FROM repos
    """

    cur.execute(sql_query)

    repo_ids = cur.fetchall()

    # flatten tuple rows into a set for O(1) search
    repo_ids = {repo_id[0] for repo_id in repo_ids}
    
    # get the length of the max commits/issues to match the sizes of commits/issues for old and new repos
    sql_query = """
        WITH count_commits_cta AS (
        	SELECT
        		repo_id,
        		COUNT(*) AS commits_count
        	FROM commits
        	GROUP BY repo_id
        )
        
        SELECT
        	MAX(commits_count)
        FROM count_commits_cta
    """

    cur.execute(sql_query)

    commits_length = cur.fetchone()[0]

    sql_query = """
        WITH count_issues_cta AS (
        	SELECT
        		repo_id,
        		COUNT(*) AS issues_count
        	FROM issues
        	GROUP BY repo_id
        )
        
        SELECT
        	MAX(issues_count)
        FROM count_issues_cta
    """

    cur.execute(sql_query)

    issues_length = cur.fetchone()[0]
    
    cur.close()

    # iterate through each user and fetch repos
    for login in logins:

        # track number of repos inserted for each user
        repo_insertion_counter = 0

        # start at page 1
        page = 1

        # iterate while the repos added is less than the max repos for this function call
        while repo_insertion_counter < num:
        
            endpoint = f"/users/{login}/repos?per_page={repo_page_size}&page={page}"

            repo_data = get_data(endpoint, headers)

            # if call returns nothing then break for current user
            # likely no more repos exist
            if repo_data == []:
                break
    
            # for each repo we will check to see if it exists in our db
            for repo in repo_data:
    
                # if it doesn't exist in the db we will add it 
                if repo['id'] not in repo_ids:
    
                    # flatten repo dictionaries
                    flatten_repo_dictionaries(repo)
    
                    # get repo name for url
                    repo_name = repo["name"]
    
                    # get repo id for flattening commits/issues dicts
                    repo_id = repo['id']
    
                    # rename repo data cols
                    normalize_data_columns(repo, rename_repos_map)
    
                    # endpoint for getting commits of a user's specific repo
                    # current commit length is less then the max pagination size
                    endpoint = f"/repos/{login}/{repo_name}/commits?per_page={commits_length}"
    
                    # returns a list
                    commit_data = get_data(endpoint, headers)
    
                    # flatten the dictionaries in each commit
                    for row in commit_data:
                
                        flatten_repo_commit_dictionaries(row, repo_id)
    
                        # rename commits data cols
                        normalize_data_columns(row, rename_commits_map)
    
                    commits_data.extend(commit_data)
    
                    # this section is to ingest issues data
                    
                    # if repo has issues then call
                    if repo["has_issues"] == True:
                        
                        # endpoint for getting issues of a user's specific repo
                        endpoint = f"/repos/{login}/{repo_name}/issues?per_page={issues_length}"
    
                        # returns list
                        issue_data = get_data(endpoint, headers)
    
                        # flatten the dictionaries in each issue 
                        for row in issue_data:
                            
                            flatten_repo_issues_dictionaries(row, repo_id)
    
                            # rename commits data cols
                            normalize_data_columns(row, rename_issues_map)
        
                        # add issue data to all issues data
                        issues_data.extend(issue_data)
    
                    # append repo 
                    repos_data.append(repo)
    
                    # increment
                    repo_insertion_counter += 1

                    # if repo_insertion_counter is equal to num then the max repos per user
                    # for this function call is reached and break out of current iteration
                    if repo_insertion_counter == num:
                        break

            # increment page
            page += 1

            # safety check break loop if max pages reached 
            if page > max_pages:
                print(f"Warning: Max pages reached for {login}")
                break
    
    # return data for insertion
    return repos_data, commits_data, issues_data

# function to ingest more commits for existing repos
def get_commits_data(num, conn, headers, rename_commits_map, **kwargs):

    # page size
    commits_length = 100

    # max pages to search through 5
    max_pages = 5

    # collect new commits
    all_commits_data = []

    cur = conn.cursor() 

    # get the user login and repo name to fetch commits for existing repos
    sql_query = """
        SELECT
        	U.login,
        	R.repo_name,
            R.repo_id
        FROM users U
        INNER JOIN repos R
        ON U.user_id = R.owner_id
    """

    cur.execute(sql_query)

    commits_endpoint_vars = cur.fetchall()
    
    # get the commits 'id' (sha) to avoid saving duplicate commits
    sql_query = """
        SELECT
            sha
        FROM commits
    """

    cur.execute(sql_query)

    commits_sha = cur.fetchall()

    # set for 0(1) search
    commits_sha = {sha[0] for sha in commits_sha}

    for cur_tuple in commits_endpoint_vars:

        # keep track of how many commits are currenlty saved
        saved_commits_counter = 0
        
        # unpack tuple
        login = cur_tuple[0]
        repo_name = cur_tuple[1]
        repo_id = cur_tuple[2]

        # init page 1
        page = 1

        # if saved_commits_counter equals num then the number of new commits for current repo is reached
        while saved_commits_counter < num:
        
            # get commits data for current user/repo
            endpoint = f"/repos/{login}/{repo_name}/commits?per_page={commits_length}&page={page}"
            commits_data = get_data(endpoint, headers)

            # if [] break to reduce calls
            if not commits_data:
                break
            
            for row in commits_data:
    
                # only flatten/rename cols/ and save commit if it is a new commit (not already in the DB)
                if row['sha'] not in commits_sha:
    
                    flatten_repo_commit_dictionaries(row, repo_id)
    
                    # rename commits data cols
                    normalize_data_columns(row, rename_commits_map)
                    
                    all_commits_data.append(row)
    
                    saved_commits_counter += 1
                    
                    # there shouldn't be dupe commits
                    commits_sha.add(row["sha"])

                    # break out of current commit data loop
                    if saved_commits_counter == num:
                        break

            # increment page
            page += 1

            # safety check break loop if max pages reached 
            if page > max_pages:
                print(f"Warning: Max pages reached for {login} and {repo_name}")
                break
        
    cur.close()

    return all_commits_data