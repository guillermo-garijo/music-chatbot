import csv

file='../data.csv'


#retorna toda la info del parametro pasado en un array
def getByParameter(parameter):
    result=[]
    with open(file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append(row[parameter])

    f.close()
    return result