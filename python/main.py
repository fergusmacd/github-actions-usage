# The starting point
import xlsxwriter as xlsxwriter

from ghaworkflows import *
from ghorg import *

LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
logging.basicConfig(format='%(asctime)s - %(levelname)s - {%(pathname)s:%(lineno)d} - %(message)s', level=LOGLEVEL)


class RepoData:

    def __str__(self):
        return "{},  UBUNTU: {}, MACOS: {}, WINDOWS: {}".format(self.name, str(self.usage["UBUNTU"]),
                                                                str(self.usage["MACOS"]),
                                                                str(self.usage["WINDOWS"]))

    def __init__(self, name, usage, actions):
        self.name = name
        self.usage = usage
        self.actions = actions


def main():
    org = os.environ['INPUT_ORGANISATION']
    logging.info("*************** Getting repos for %s ***************", org)

    repoNames = getreposfromorganisation(org)
    totalRepos = len(repoNames)
    logging.info("*************** totalRepos %s ***************", totalRepos)

    reposUsage = []
    totalCosts = dict.fromkeys(['UBUNTU', 'MACOS', 'WINDOWS'], 0)
    for repoName in repoNames:
        actions = []
        repoData = RepoData(repoName, dict.fromkeys(['UBUNTU', 'MACOS', 'WINDOWS'], 0), actions)
        logging.info("*************** Repo Name %s ***************", repoData.name)

        getrepoworkflows(org, repoData)
        reposUsage.append(repoData)
        logging.info("*************** Repo Usage Summary %s ***************", repoData.usage)
        logging.info("\n\n")
        totalCosts["UBUNTU"] += repoData.usage["UBUNTU"]
        totalCosts["MACOS"] += repoData.usage["MACOS"]
        totalCosts["WINDOWS"] += repoData.usage["WINDOWS"]

    logging.info("**********************************************")
    logging.info("*************** Total Costs %s ***************", totalCosts)

    workbook = xlsxwriter.Workbook(org + ".xlsx")
    worksheet = workbook.add_worksheet()
    detailedWorksheet = workbook.add_worksheet()
    row = 0
    worksheet.write(row, 0, "Repo Name")
    worksheet.write(row, 1, "MacOS")
    worksheet.write(row, 2, "Ubuntu")
    worksheet.write(row, 3, "Windows")

    detailedWorksheet.write(row, 0, "Repo Name")
    detailedWorksheet.write(row, 1, "MacOS")
    detailedWorksheet.write(row, 2, "MacOS")
    detailedWorksheet.write(row, 3, "Ubuntu")
    detailedWorksheet.write(row, 4, "Windows")

    # increment the row
    row = 1
    for repo in reposUsage:
        logging.info("*************** Repo name %s ***************", repo.name)
        col = 0
        worksheet.write(row, col, repo.name)
        worksheet.write(row, col + 1, repo.usage["MACOS"])
        worksheet.write(row, col + 2, repo.usage["UBUNTU"])
        worksheet.write(row, col + 3, repo.usage["WINDOWS"])
        row = row + 1
        for action in repo.actions:
            logging.info("*************** Action name and usage: %s ***************", action)

    # Write a total using a formula.
    macOSFormula = "=SUM(B1:B{})".format(row - 1)
    ubuntuOSFormula = "=SUM(C1:C{})".format(row - 1)
    windowsOSFormula = "=SUM(D1:D{})".format(row - 1)
    worksheet.write(row, 0, 'Totals')
    worksheet.write(row, 1, macOSFormula)
    worksheet.write(row, 2, ubuntuOSFormula)
    worksheet.write(row, 3, windowsOSFormula)

    workbook.close()


if __name__ == "__main__":
    main()
