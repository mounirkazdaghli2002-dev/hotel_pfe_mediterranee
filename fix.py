import pandas as pd
df = pd.read_csv('chambres.csv')
df['statut'] = 'Libre'
df.to_csv('chambres.csv', index=False)
print('OK')

