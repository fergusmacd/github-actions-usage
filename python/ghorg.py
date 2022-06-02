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
    perPage = 100
    # get total repos
    api_url = 'https://api.github.com/orgs/{}'.format(org)

    logger.info(f'Data from api_url: {api_url}')
    response = requests.get(api_url, headers=headers)
    json_data = json.loads(response.text)

    logger.debug(f'Data from org: {json_data}')
    totalPrivateRepos = json_data["total_private_repos"]
    logger.info(f"Total private repos: {totalPrivateRepos}")
    totalPublicRepos = json_data["public_repos"]
    logger.info(f'Total public repos: {totalPublicRepos}')
    totalRepos = totalPrivateRepos + totalPublicRepos
    logger.info(f'Total repos: {totalRepos}')

    pageUntil = int(totalRepos / perPage) + (totalRepos % perPage > 0)
    logger.debug(f'Pages: {pageUntil}')
    repos = []
    for page in range(pageUntil):
        api_url = 'https://api.github.com/orgs/{}/repos?page={}&per_page={}'.format(org, page + 1, perPage)
        logger.debug(f'Calling: {api_url}')
        response = requests.get(api_url, headers=headers)
        json_data = json.loads(response.text)

        for repo in json_data:
            repos.append(repo["name"])

    return repos
