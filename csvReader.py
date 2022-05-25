import csv

def csvRead(fileName):
    review = []
    with open(fileName) as file:
        csvReader = csv.reader(file, delimiter=',')
        for row in csvReader:
            review.append(row)
    return review