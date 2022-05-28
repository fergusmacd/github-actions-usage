import json

import requests

from common import *

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(format='%(asctime)s - %(levelname)s - {%(pathname)s:%(lineno)d} - %(message)s', level=LOGLEVEL)

# get any header or key values we need
github_api_key = getgithubapikey()
headers = {"Authorization": "token {}".format(github_api_key),
           "Accept": "application/vnd.github.v3+json"}


class Action:

    def __init__(self, name, workflow):
        self.name = name
        self.workflow = workflow

    def __str__(self):
        return "{},  UBUNTU: {}, MACOS: {}, WINDOWS: {}".format(self.name, str(self.workflow["UBUNTU"]),
                                                                str(self.workflow["MACOS"]),
                                                                str(self.workflow["WINDOWS"]))


def getrepoworkflows(org: object, repo: object) -> object:
    api_url = 'https://api.github.com/repos/{}/{}/actions/workflows'.format(org, repo.name)
    # call the API
    response = requests.get(api_url, headers=headers)
    # Convert the data to a dictionary
    json_data = json.loads(response.text)

    delimiter = "/"
    for workflow in json_data["workflows"]:
        workflowPath = workflow["path"]
        workflowName = workflowPath[workflowPath.rindex(delimiter) + 1:]
        logging.info("*************** workflow name: %s , id: %s ***************", workflowName, workflow["id"])
        getrepoworkflowminutes(org, repo, workflowName, workflow["id"])

    logging.info("*************** total usage: %s for repo: %s ***************", repo.usage, repo.name)
    return repo


def getrepoworkflowminutes(orgName, repo, workflowName, workflowId):
    # the server bombs out if we use the workflow name and it has underscore! So use ID
    repo_api_url = 'https://api.github.com/repos/{}/{}/actions/workflows/{}/timing'.format(orgName, repo.name,
                                                                                           workflowId)
    response = requests.get(repo_api_url, headers=headers)
    # Convert the data to a dictionary
    json_data = json.loads(response.text)
    action = Action(workflowName, dict.fromkeys(['UBUNTU', 'MACOS', 'WINDOWS'], 0))
    try:
        if "MACOS" in json_data["billable"]:
            milliseconds = json_data["billable"]["MACOS"]["total_ms"]
            minutes = int((milliseconds / (1000 * 60) * 10))
            repo.usage["MACOS"] += minutes
            action.workflow["MACOS"] = minutes
    except KeyError:
        logging.info("*************** json_data %s , repo: %s, workflow: %s, workflow id: %s ***************",
                     json_data, repo.name, workflowName, workflowId)

    try:
        if "UBUNTU" in json_data["billable"]:
            milliseconds = json_data["billable"]["UBUNTU"]["total_ms"]
            minutes = int((milliseconds / (1000 * 60)))
            repo.usage["UBUNTU"] += minutes
            action.workflow["UBUNTU"] = minutes
    except KeyError:
        logging.info("*************** json_data %s , repo: %s, workflow: %s, workflow id: %s ***************",
                     json_data, repo.name, workflowName, workflowId)

    try:
        if "WINDOWS" in json_data["billable"]:
            milliseconds = json_data["billable"]["WINDOWS"]["total_ms"]
            minutes = int((milliseconds / (1000 * 60)))
            repo.usage["WINDOWS"] += minutes
            action.workflow["WINDOWS"] = minutes
    except KeyError:
        logging.info("*************** json_data %s , repo: %s, workflow: %s, workflow id: %s ***************",
                     json_data, repo.name, workflowName, workflowId)

    repo.actions.append(action)
    logging.info("*************** action %s ***************", action)
