import csv
import csvData

def csvRead(fileName):
    dashboardData = []
    with open(fileName) as file:
        csvReader = csv.reader(file, delimiter=',')
        for row in csvReader:
            dashboardData.append(row)
    return dashboardData