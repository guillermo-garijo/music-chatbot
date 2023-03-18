import csv
import os
import pandas

# Define the relative path to the file
relative_path = os.path.join('../data', 'data.csv')

# Construct the absolute path to the file
absolute_path = os.path.abspath(relative_path)

#retorna toda la info del parametro pasado en un array
def getByParameter(parameter):
    result=[]
    with open(absolute_path, 'r', encoding='utf-8') as f:
        reader = pandas.read_csv(f)
        for p in parameter:
            result.append(reader.loc[: , p])
        f.close()
    return result
