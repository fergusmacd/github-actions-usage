import json

import requests

from common import getgithubapikey
from customlogger import getlogger

# Set the header values
github_api_key = getgithubapikey()
headers = {"Authorization": "token {}".format(github_api_key),
           "Accept": "application/vnd.github.v3+json"}

logger = getlogger()


# Get the repos for the org, and the total number
def getreposfromorganisation(org):
    per_page = 100
    # get total repos
    api_url = 'https://api.github.com/orgs/{}'.format(org)

    logger.info(f'Data from api_url: {api_url}')
    response = requests.get(api_url, headers=headers)
    json_data = json.loads(response.text)

    logger.debug(f'Data from org: {json_data}')
    total_private_repos = json_data["total_private_repos"]
    logger.info(f"Total private repos: {total_private_repos}")
    total_public_repos = json_data["public_repos"]
    logger.info(f'Total public repos: {total_public_repos}')
    total_repos = total_private_repos + total_public_repos
    logger.info(f'Total repos: {total_repos}')

    page_until = int(total_repos / per_page) + (total_repos % per_page > 0)
    logger.debug(f'Pages: {page_until}')
    repos = []

    for page in range(page_until):
        api_url = 'https://api.github.com/orgs/{}/repos?page={}&per_page={}'.format(org, page + 1, per_page)
        logger.debug(f'Calling: {api_url}')
        response = requests.get(api_url, headers=headers)
        json_data = json.loads(response.text)

        for repo in json_data:
            repos.append(repo["name"])

    repos.sort()
    return repos
