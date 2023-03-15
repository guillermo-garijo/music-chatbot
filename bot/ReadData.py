import csv

file='data.csv'


#retorna toda la info del parametro pasado en un array
def getByParameter(parameter):
    result=[]
    with open(file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tmp=[]
            for p in parameter:
                tmp.append(row[p])
            result.append(tmp)
    f.close()
    return result