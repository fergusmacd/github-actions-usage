# The starting point
import xlsxwriter as xlsxwriter

from python.customlogger import getlogger

logger = getlogger()


def printxls(org, repos_usage):
    workbook = xlsxwriter.Workbook(org + ".xlsx")
    worksheet = workbook.add_worksheet()
    detailed_worksheet = workbook.add_worksheet()
    row = 0
    worksheet.write(row, 0, "Repo Name")
    worksheet.write(row, 1, "Ubuntu")
    worksheet.write(row, 2, "MacOS")
    worksheet.write(row, 3, "Windows")

    detailed_worksheet.write(row, 0, "Repo Name")
    detailed_worksheet.write(row, 1, "Workflow")
    detailed_worksheet.write(row, 2, "Ubuntu")
    detailed_worksheet.write(row, 3, "MacOS")
    detailed_worksheet.write(row, 4, "Windows")

    # increment the row
    row = 1
    for repo in repos_usage:
        col = 0
        worksheet.write(row, col, repo.name)
        worksheet.write(row, col + 1, repo.usage["UBUNTU"])
        worksheet.write(row, col + 2, repo.usage["MACOS"])
        worksheet.write(row, col + 3, repo.usage["WINDOWS"])
        row = row + 1
    #        for action in repo.actions:

    # Write a total using a formula.
    ubuntu_os_formula = "=SUM(B1:B{})".format(row - 1)
    mac_os_formula = "=SUM(C1:C{})".format(row - 1)
    windows_os_formula = "=SUM(D1:D{})".format(row - 1)
    worksheet.write(row, 0, 'Totals')
    worksheet.write(row, 1, ubuntu_os_formula)
    worksheet.write(row, 2, mac_os_formula)
    worksheet.write(row, 3, windows_os_formula)
    workbook.close()
