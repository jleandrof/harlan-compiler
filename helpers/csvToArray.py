import csv

with open("input.txt", "r") as f:

    result = []
    csvFile = csv.reader(f, delimiter="\t")
    for row in csvFile:
        result.append([int(r) if(len(r) >  0) else -1 for r in row])

    print(result)
