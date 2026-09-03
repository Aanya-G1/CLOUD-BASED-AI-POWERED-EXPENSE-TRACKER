import pandas as pd

data= {
    'description': ['Uber ride','Lunch at Subway','Movie ticket','Electricity bill','Bus ticket','Netflix subscription','Dinner at KFC','Flight','Taxi','Mobile recharge','recharge','restaurant','Grocery','Amazon','H&M','courses','Books','stationery','school','hospital','doctor','medicine','gym','Insurance','Mutual funds','stocks','coffee','tea','snacks','lunch'],
    'category': ['Travel','Food','Entertainment','Bills','Travel','Entertainment','Food','Travel','Travel','Bills','Bills','Food','Food','Shopping','Shopping','Education','Education','Education','Education','health','health','health','health','Investment','Investment','Investment','Food','Food','Food','Food']
}
df= pd.DataFrame(data)
df.to_csv('expenses_dataset.csv', index=False)