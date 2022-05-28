import json
import logging

import requests

from common import *

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(format='%(asctime)s - %(levelname)s - {%(pathname)s:%(lineno)d} - %(message)s', level=LOGLEVEL)

# Set the header values
github_api_key = getGitHubAPIKey()
headers = {"Authorization": "token {}".format(github_api_key),
           "Accept": "application/vnd.github.v3+json"}


# Get the repos for the org, and the total number
def getreposfromorganisation(org):
    perPage = 100
    # get total repos
    api_url = 'https://api.github.com/orgs/{}'.format(org)
    print(api_url)
    logging.debug("Data from api_url: %s", api_url)
    response = requests.get(api_url, headers=headers)
    json_data = json.loads(response.text)
    print(json_data)
    logging.debug("Data from org: %s", json_data)
    totalPrivateRepos = json_data["total_private_repos"]
    logging.debug("Total private repos: %s", totalPrivateRepos)
    totalPublicRepos = json_data["public_repos"]
    logging.debug("Total public repos: %s", totalPublicRepos)
    totalRepos = totalPrivateRepos + totalPublicRepos
    logging.debug("Total repos: %s", totalRepos)

    pageUntil = int(totalRepos / perPage) + (totalRepos % perPage > 0)
    logging.debug("Pages: %s", pageUntil)
    repos = []
    for page in range(pageUntil):
        api_url = 'https://api.github.com/orgs/{}/repos?page={}&per_page={}'.format(org, page + 1, perPage)
        logging.info("Calling: %s", api_url)
        response = requests.get(api_url, headers=headers)
        json_data = json.loads(response.text)

        for repo in json_data:
            repos.append(repo["name"])

    return repos
