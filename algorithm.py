import pandas as pd
import itertools

min_support_count =0.0
min_confidence = 0.0
sample = None


def preprocessInputs(filePath, min_sub, min_con, percentage):
    global min_support_count, min_confidence, sample
    df = pd.read_csv(filePath)
    df.drop(['DateTime', 'Daypart', 'DayType'], axis=1, inplace=True)
    min_support_count = min_sub 
    min_confidence = min_con
    num_desired_records = int(len(df) * float(percentage) / 100)
    sample = df.sample(n=num_desired_records)


def constructTransactions():
    transactions ={}
    support_counts ={}
    for index, record in sample.iterrows():
        if record["TransactionNo"] in transactions.keys() :
            existed =False
            for p in transactions[record["TransactionNo"]].split(","):
                if p ==record["Items"]:
                    existed = True
                    break
            if not existed :
                if (record["Items"],) in support_counts.keys():
                    support_counts[(record["Items"],)] += 1 
                else :
                     support_counts[(record["Items"],)] = 1
            else:
                existed = False
            transactions[record["TransactionNo"]] += "," + str(record["Items"])     
            
        else:
            if (record["Items"],) in support_counts.keys():
                    support_counts[(record["Items"],)] += 1 
            else :
                    support_counts[(record["Items"],)] = 1    
            transactions[record["TransactionNo"]] = str(record["Items"] )

    print("Transactions")
    for i , t in transactions.items():
        print(i ," : ", t)
    print("------------------------------")
    return transactions, support_counts     


def getFrequentItemSets(transactions, support_counts):
    res =""
    itemsetSize =2
    products = set([(key[0]) if len(key) == 1 else key for key in support_counts.keys()])
    passed = []
    largest_frequent_itemsets=[]
  
    for item , sup_count in  list(support_counts.items()):
        if sup_count< min_support_count:
            del support_counts[item]     

    while products :
        res += "\n Frequent "+ str(itemsetSize)+"-itemset \n"
        itemsets = list(itertools.combinations(products, itemsetSize))   
        products = set()
        largest_frequent_itemsets= list(passed)
        passed =[]
        
        for itemset in itemsets:
            itemset = tuple(sorted(itemset))
            supp_count =0
            
            for  t in transactions.values(): 
                if all(item in t.split(',') for item in itemset): 
                    supp_count += 1 
           
            if supp_count >= min_support_count:
                if len(itemset) ==1:
                    itemset = itemset,
                support_counts[itemset]=supp_count
                passed.append(itemset)  
                res += str (itemset)
                res += "\n"
                products |= set(itemset)
            
        itemsetSize +=1

    print("support counts")
    print(support_counts)
    print("------------------------------")
        
    return res, support_counts, largest_frequent_itemsets


def getStrongAssociationRules(support_counts, frequentItemsets):
    print("Association rules")
    confidence = 0
    result =""
    strongAssociationRules = []
    for frequentItemset in frequentItemsets:
        for i in range (1,len(frequentItemset)):
            for first in itertools.combinations(frequentItemset, i):
                first = tuple(sorted(first))         
                second = tuple(set(frequentItemset)-set(first))
                print(first," -> ",second," = ",(support_counts[frequentItemset]/support_counts[first])*100)

                confidence = (support_counts[frequentItemset]/support_counts[first])*100
                if confidence >= min_confidence :
                    strongAssociationRules.append(str(first)+" -> "+str(second))
                    result += str(first)+" -> "+str(second)+" = "+str(confidence)+ " %"+"\n"

    return result, strongAssociationRules          
                


def Apriori(filePa, min_sub,min_con, percentage):
    preprocessInputs( filePa, min_sub,min_con, percentage)
    transactions, support_counts = constructTransactions()
    result1, support_counts, frequentItemsets = getFrequentItemSets(transactions, support_counts)
    result2, strongAssociationRules = getStrongAssociationRules(support_counts, frequentItemsets)
    return result1, result2