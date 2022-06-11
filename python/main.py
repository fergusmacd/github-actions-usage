# The starting point
import os

from prettytable import PrettyTable

from python.customlogger import getlogger
from python.ghaworkflows import getrepoworkflows
from python.ghorg import getreposfromorganisation


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

repo_name_column_header = "Repo Name"


def main():
    org = os.environ['INPUT_ORGANISATION']

    logger.info(f'*************** Getting repos for {org} ***************')
    # Get all the repo names for the org, will page results too
    # repo names are returned sorted
    repoNames = getreposfromorganisation(org)

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
    workflow_table: PrettyTable = PrettyTable()
    workflow_table.field_names = [repo_name_column_header, "Workflow", "Ubuntu", "MacOS", "Windows"]
    workflow_table.align[repo_name_column_header] = "l"
    workflow_table.align["Workflow"] = "l"
    summary_table: PrettyTable = PrettyTable()
    summary_table.field_names = [repo_name_column_header, "Ubuntu", "MacOS", "Windows"]
    summary_table.align[repo_name_column_header] = "l"

    for repo in reposUsage:
        summary_table.add_row([repo.name, repo.usage["UBUNTU"], repo.usage["MACOS"], repo.usage["WINDOWS"]])
        first_row: bool = True
        if not repo.actions:
            workflow_table.add_row([repo.name, "No workflows", "0", "0", "0"])
        for action in repo.actions:
            if first_row:
                workflow_table.add_row([repo.name, action.name, action.workflow['UBUNTU'], action.workflow['MACOS'],
                                        action.workflow['WINDOWS']])
                first_row = False
            else:
                workflow_table.add_row(["", action.name, action.workflow['UBUNTU'], action.workflow['MACOS'],
                                        action.workflow['WINDOWS']])
        workflow_table.add_row(["--------", "--------", "-----", "-----", "-----"])

    summary_table.add_row(["---------", "----", "----", "----"])
    summary_table.add_row(["Total Costs", totalCosts["UBUNTU"], totalCosts["MACOS"], totalCosts["WINDOWS"]])
    summary_table.add_row(["---------", "----", "----", "----"])
    print(summary_table)
    print(workflow_table)


if __name__ == "__main__":
    main()
