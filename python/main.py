# The starting point
import os
from datetime import datetime

from prettytable import PrettyTable

from customlogger import getlogger
from ghaworkflows import getrepoworkflows
from ghorg import getreposfromorganisation, getremainingdaysinbillingperiod, gettotalghausage


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
datetime_format = "%Y-%m-%d %H:%M"


def main():
    org = os.environ['INPUT_ORGANISATION']

    logger.info(f'*************** Getting repos for {org} ***************')
    # Get all the repo names for the org, will page results too
    # repo names are returned sorted
    repo_names = getreposfromorganisation(org)
    billing_days_left = getremainingdaysinbillingperiod(org)
    repos_usage = []
    total_costs = dict.fromkeys(['UBUNTU', 'MACOS', 'WINDOWS'], 0)
    # Collect the data from each repo
    for repo_name in repo_names:
        actions = []
        repo_data = RepoData(repo_name, dict.fromkeys(['UBUNTU', 'MACOS', 'WINDOWS'], 0), actions)
        logger.info(f"*************** Repo Name {repo_data.name} ***************")
        getrepoworkflows(org, repo_data)
        repos_usage.append(repo_data)
        logger.info(f"*************** Repo Usage Summary {repo_data.usage} ***************")
        total_costs["UBUNTU"] += repo_data.usage["UBUNTU"]
        total_costs["MACOS"] += repo_data.usage["MACOS"]
        total_costs["WINDOWS"] += repo_data.usage["WINDOWS"]

    logger.info(f"***************Total Costs: {total_costs} *******************")
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
    validate_total_costs = dict.fromkeys(['UBUNTU', 'MACOS', 'WINDOWS'], 0)
    for repo in repos_usage:
        summary_table.add_row([repo.name, repo.usage["UBUNTU"], repo.usage["MACOS"], repo.usage["WINDOWS"]])
        first_row: bool = True
        if not repo.actions:
            workflow_table.add_row([repo.name, "No workflows", "0", "0", "0"])
        for action in repo.actions:
            if first_row:
                workflow_table.add_row([repo.name, action.name, action.workflow['UBUNTU'], action.workflow['MACOS'],
                                        action.workflow['WINDOWS']])
                first_row = False
                validate_total_costs["UBUNTU"] += action.workflow["UBUNTU"]
                validate_total_costs["MACOS"] += action.workflow["MACOS"]
                validate_total_costs["WINDOWS"] += action.workflow["WINDOWS"]
            else:
                workflow_table.add_row(["", action.name, action.workflow['UBUNTU'], action.workflow['MACOS'],
                                        action.workflow['WINDOWS']])
                validate_total_costs["UBUNTU"] += action.workflow["UBUNTU"]
                validate_total_costs["MACOS"] += action.workflow["MACOS"]
                validate_total_costs["WINDOWS"] += action.workflow["WINDOWS"]

        workflow_table.add_row(["--------", "--------", "-----", "-----", "-----"])

    # get what GH thinks our usage is
    monthly_usage_dic = gettotalghausage(org)
    monthly_usage_breakdown_dic = monthly_usage_dic["minutes_used_breakdown"]
    included_minutes = monthly_usage_dic["included_minutes"]
    total_minutes_used = monthly_usage_dic["total_minutes_used"]
    total_paid_minutes_used = monthly_usage_dic["total_paid_minutes_used"]
    raise_alarm_remaining_minutes = os.environ['INPUT_RAISEALARMREMAININGMINUTES']
    remaining_minutes = included_minutes - total_minutes_used

    summary_table.add_row(["---------", "----", "----", "----"])
    summary_table.add_row(
        ["Usage Minutes " + datetime.now().strftime(datetime_format), total_costs["UBUNTU"],
         total_costs["MACOS"],
         total_costs["WINDOWS"]])
    summary_table.add_row(["---------", "----", "----", "----"])
    summary_table.add_row(["Stats From GitHub", "", "", ""])
    summary_table.add_row(["Monthly Allowance: " + str(included_minutes), "", "", ""])
    summary_table.add_row(["Usage Minutes: " + str(total_minutes_used),
                           monthly_usage_breakdown_dic["UBUNTU"], monthly_usage_breakdown_dic["MACOS"],
                           monthly_usage_breakdown_dic["WINDOWS"]])
    summary_table.add_row(["Remaining Minutes: " + str(remaining_minutes), "", "", ""])
    summary_table.add_row(["Alarm Triggered at: " + raise_alarm_remaining_minutes, "", "", ""])
    summary_table.add_row(["Paid Minutes: " + str(total_paid_minutes_used), "", "", ""])
    summary_table.add_row(["Days Left in Cycle: " + str(billing_days_left), "", "", ""])
    workflow_table.add_row(["Usage Minutes " + datetime.now().strftime(datetime_format), "",
                            validate_total_costs["UBUNTU"], validate_total_costs["MACOS"],
                            validate_total_costs["WINDOWS"]])
    workflow_table.add_row(["--------", "--------", "-----", "-----", "-----"])
    workflow_table.add_row(["Stats From GitHub", "", "", "", ""])
    workflow_table.add_row(["Monthly Allowance: " + str(included_minutes), "", "", "", ""])
    workflow_table.add_row(["Usage Minutes: " + str(total_minutes_used), "",
                            monthly_usage_breakdown_dic["UBUNTU"], monthly_usage_breakdown_dic["MACOS"],
                            monthly_usage_breakdown_dic["WINDOWS"]])
    workflow_table.add_row(["Remaining Minutes: " + str(remaining_minutes), "", "", "", ""])
    workflow_table.add_row(["Alarm Triggered at: " + raise_alarm_remaining_minutes, "", "", "", ""])
    workflow_table.add_row(["Paid Minutes: " + str(total_paid_minutes_used), "", "", "", ""])

    workflow_table.add_row(["Days Left in Cycle: " + str(billing_days_left), "", "", "", ""])
    print(summary_table)
    print(workflow_table)
    # we should throw an error if we are running out of minutes as a warning
    # minutes buffer is how low the minutes should get before failing and raising an alarm
    if remaining_minutes < int(raise_alarm_remaining_minutes):
        raise Exception(f'Your organisation is running short on minutes, you have {raise_alarm_remaining_minutes} left')


if __name__ == "__main__":
    main()
