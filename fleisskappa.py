kdf = dfpayloads[['annotation', 'task_id', 'payload', 'user_id']] 
# payload is not unique, so I made one. confirmed unique
kdf['unique'] = (kdf.task_id).apply(lambda x: str(x)) + (kdf.payload).apply(lambda x: str(x))

# get a count for annotation per task payload
kdf = pd.concat([kdf, (pd.get_dummies(kdf['annotation']))], axis =1)
df1 = (kdf.groupby([ 'unique', ]).sum()['duplicate'].to_frame().reset_index())
df2 = (kdf.groupby([ 'unique', ]).sum()['non-duplicate'].to_frame().reset_index())
df3 = (kdf.groupby([ 'unique', ]).sum()['unsure'].to_frame().reset_index())
kap = pd.merge(df1,df2, on = 'unique')
kap = pd.merge(df3, kap, on = 'unique' )

n = 5 # of unique raters
N = len(kap.unique.unique()) #number of tasks

## Calculations
kap["Pi"] = (((kap['duplicate']**2 + kap['non-duplicate']**2) + kap['unsure']**2) - n)*(1/(n*(n-1)))
Pbar = (np.sum(kap["Pi"]))*(1/N)

p1 = []


for i,v in enumerate(['duplicate', 'non-duplicate', 'unsure']):
    p = (np.sum(kap[str(v)]))/ (n*N)
    p1.append(p)

    
Pbare = np.sum([x**2 for x in p1])
Kappa = (Pbar - Pbare) / (1-Pbare)
print(Kappa)
