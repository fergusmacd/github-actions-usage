# The starting point
from prettytable import PrettyTable

from ghaworkflows import *
from ghorg import *


class RepoData:

    def __str__(self):
        return "{},  UBUNTU: {}, MACOS: {}, WINDOWS: {}".format(self.name, str(self.usage["UBUNTU"]),
                                                                str(self.usage["MACOS"]),
                                                                str(self.usage["WINDOWS"]))

    def __init__(self, name, usage, actions):
        self.name = name
        self.usage = usage
        self.actions = actions


logger = getlogger()


def main():
    org = os.environ['INPUT_ORGANISATION']

    logger.info(f'*************** Getting repos for {org} ***************')
    # Get all the repo names for the org, will page results too
    # repo names are returned sorted
    repoNames = getreposfromorganisation(org)
    # totalRepos = len(repoNames)

    reposUsage = []
    totalCosts = dict.fromkeys(['UBUNTU', 'MACOS', 'WINDOWS'], 0)
    # Collect the data from each repo
    for repoName in repoNames:
        actions = []
        repoData = RepoData(repoName, dict.fromkeys(['UBUNTU', 'MACOS', 'WINDOWS'], 0), actions)
        logger.info(f"*************** Repo Name {repoData.name} ***************")
        getrepoworkflows(org, repoData)
        reposUsage.append(repoData)
        logger.info(f"*************** Repo Usage Summary {repoData.usage} ***************")
        totalCosts["UBUNTU"] += repoData.usage["UBUNTU"]
        totalCosts["MACOS"] += repoData.usage["MACOS"]
        totalCosts["WINDOWS"] += repoData.usage["WINDOWS"]

    logger.info(f"***************Total Costs: {totalCosts} *******************")
    # table tp print out per repo/workflow
    # Repo names are already sorted and we don't want to sort on tables
    # as order would mess up with totals
    workflowTable = PrettyTable()
    workflowTable.field_names = ["Repo Name", "Workflow", "Ubuntu", "MacOS", "Windows"]
    workflowTable.align["Repo Name"] = "l"
    workflowTable.align["Workflow"] = "l"
    summaryTable = PrettyTable()
    summaryTable.field_names = ["Repo Name", "Ubuntu", "MacOS", "Windows"]
    summaryTable.align["Repo Name"] = "l"

    for repo in reposUsage:
        summaryTable.add_row([repo.name, repo.usage["UBUNTU"], repo.usage["MACOS"], repo.usage["WINDOWS"]])
        firstRow: bool = True
        if not repo.actions:
            workflowTable.add_row([repo.name, "No workflows", "0", "0", "0"])
        for action in repo.actions:
            if firstRow:
                workflowTable.add_row([repo.name, action.name, action.workflow['UBUNTU'], action.workflow['MACOS'],
                                       action.workflow['WINDOWS']])
                firstRow = False
            else:
                workflowTable.add_row(["", action.name, action.workflow['UBUNTU'], action.workflow['MACOS'],
                                       action.workflow['WINDOWS']])
        workflowTable.add_row(["--------", "--------", "-----", "-----", "-----"])

    summaryTable.add_row(["---------", "----", "----", "----"])
    summaryTable.add_row(["Total Costs", totalCosts["UBUNTU"], totalCosts["MACOS"], totalCosts["WINDOWS"]])
    summaryTable.add_row(["---------", "----", "----", "----"])
    print(summaryTable)
    print(workflowTable)


if __name__ == "__main__":
    main()
