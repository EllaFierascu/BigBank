from calcBank import calcInstallment, calcBalance, getNoTotalPayments
import pandas as pd
import os

def loadDatabase():
    #The loans will be added in the csv file
    #get the path to the csv file and join it with the file name
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "BigBank_situation.csv")
    #read the csv file from the path
    df = pd.read_csv(file_path, delimiter=',')
    entries = df.to_dict()  
    
    #get keys and values from the dictonary with dictionaries
    keys = entries.keys()
    values = entries.values()

    #get a list with dictionaries created from values
    dataset = zip(*map(lambda x: x.values(), values))
    # 
    store = []
    for i, data in enumerate(dataset):
        row = {}
        for idx, val in enumerate(data):
            #create a dictionary by adding the initial key and value (ex: val) from one of the dictionaries (ex: data)
            row[keys[idx]] = val
        #append arranged dictionaries to the list
        store.append(row)
    
    return store
    
def main():
    db = loadDatabase()

    def populate(entry):
        #populates Installment value by using the function calcInstallment
        entry["installment"] = calcInstallment(entry)
        #populates Number of payments value by using the function getNoTotalPayments
        entry["no_payments"] = getNoTotalPayments(entry)
        #populates Balance value by using the function calcBalance
        entry["balance"] = calcBalance(entry)
        return entry
    
    db = map(populate, db)
    print db
        

if __name__ == "__main__":
    main()
    