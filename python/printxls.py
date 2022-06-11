# The starting point
import xlsxwriter as xlsxwriter

from ghorg import *

logger = getlogger()


def printxls(org, reposUsage):
    workbook = xlsxwriter.Workbook(org + ".xlsx")
    worksheet = workbook.add_worksheet()
    detailedWorksheet = workbook.add_worksheet()
    row = 0
    worksheet.write(row, 0, "Repo Name")
    worksheet.write(row, 1, "Ubuntu")
    worksheet.write(row, 2, "MacOS")
    worksheet.write(row, 3, "Windows")

    detailedWorksheet.write(row, 0, "Repo Name")
    detailedWorksheet.write(row, 1, "Workflow")
    detailedWorksheet.write(row, 2, "Ubuntu")
    detailedWorksheet.write(row, 3, "MacOS")
    detailedWorksheet.write(row, 4, "Windows")

    # increment the row
    row = 1
    for repo in reposUsage:
        col = 0
        worksheet.write(row, col, repo.name)
        worksheet.write(row, col + 1, repo.usage["UBUNTU"])
        worksheet.write(row, col + 2, repo.usage["MACOS"])
        worksheet.write(row, col + 3, repo.usage["WINDOWS"])
        row = row + 1
    #        for action in repo.actions:

    # Write a total using a formula.
    ubuntuOSFormula = "=SUM(B1:B{})".format(row - 1)
    macOSFormula = "=SUM(C1:C{})".format(row - 1)
    windowsOSFormula = "=SUM(D1:D{})".format(row - 1)
    worksheet.write(row, 0, 'Totals')
    worksheet.write(row, 1, ubuntuOSFormula)
    worksheet.write(row, 2, macOSFormula)
    worksheet.write(row, 3, windowsOSFormula)
    workbook.close()
