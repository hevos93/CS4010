import pandas as pd

# Setup
fileName = "<InsertFilenameHere>"
pd.set_option('expand_frame_repr', False)

# Read xlsx file
df = pd.concat(pd.read_excel(f'../raw-data/{fileName}.xlsx', sheet_name=None), ignore_index=True) # Gather all sheets from excel workbook to single dataframe

# Remove non number values
df['Trafikkmengde'] = pd.to_numeric(df['Trafikkmengde'], errors='coerce')
df['Gyldige passeringer'] = pd.to_numeric(df['Gyldige passeringer'], errors='coerce')
df['Gjennomsnittshastighet'] = pd.to_numeric(df['Gjennomsnittshastighet'], errors='coerce')
df['85-fraktil'] = pd.to_numeric(df['85-fraktil'], errors='coerce')
df = df.dropna(subset=['Trafikkmengde', 'Gyldige passeringer', 'Gjennomsnittshastighet', '85-fraktil'])

# Sum numerical values for the two different lanes to one (Use sum and mean as appropriate)
df = df.groupby(['Trafikkregistreringspunkt','Vegreferanse','Navn','Dato', 'Fra tidspunkt', 'Til tidspunkt']).agg(
    {'Trafikkmengde': 'sum', 'Gyldige passeringer': 'sum', 'Gjennomsnittshastighet':'mean', '85-fraktil':'mean'}
).reset_index()
df.columns = ['Trafikkregistreringspunkt','Vegreferanse','Navn','Dato', 'Fra tidspunkt', 'Til tidspunkt', 'Trafikkmengde', 'Gyldige passeringer', 'Gjennomsnittshastighet', '85-fraktil']

# Round mean columns to 1 decimal
df['Gjennomsnittshastighet'] = df['Gjennomsnittshastighet'].round(1)
df['85-fraktil'] = df['85-fraktil'].round(1)

# Save to csv
df.to_csv(f'../datasets/{fileName}.csv', index=False, quoting=1)