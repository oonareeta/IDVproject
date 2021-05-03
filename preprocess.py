import pandas as pd
import pycountry

# Load data
df = pd.read_csv("orig_data.csv")

# Remove others than European countries
europe = pd.read_csv("eurcountries.csv", names=['country', 'population', 'area'])
europe = europe['country'].to_list()

# Manually change country names that differ in the two datasets
europe[0] = 'Russian Federation'
europe[11] = 'Czech Republic'
europe[31] = 'The former Yugoslav Republic of Macedonia'

df['In Europe'] = False

for i in range(len(df)):
    if df['Country'].loc[i] in europe:
        df['In Europe'].loc[i] = True

df = df.drop(df[df['In Europe'] == False].index)

# Add contry codes to df
input_countries = list(df['Country'])

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country, 'Unknown code') for country in input_countries]

df['Codes'] = codes

# Drop non-used columns
dff = df.copy()
dff = dff.drop(columns=['In Europe', 'Hobbyist', 'EdLevel', 'Employment',
       'OrgSize', 'UndergradMajor', 'YearsCodePro',
       'Data scientist or machine learning specialist',
       'Database administrator', 'Data or business analyst', 'Engineer, data'])

# Get median salaries
df1 = dff.groupby(['Country', 'Codes', 'Year'])[['ConvertedComp']].median()
df1.reset_index(inplace=True)

# Get mean job satisfaction rates
df2 = dff.groupby(['Country', 'Codes', 'Year'])[['JobSat']].mean()
df2.reset_index(inplace=True)

# Make final dataframe, add "combined" column
df = df1
df["JobSat"] = df2["JobSat"]

max_salary = max(df["ConvertedComp"])
max_sat = max(df["JobSat"])

df['Combined'] = 0

for i in range(len(df)):
    df['Combined'] = (df['ConvertedComp']/max_salary + df['JobSat']/max_sat)*10 / 2

df = df.rename(columns = {'ConvertedComp': 'Salary', 'JobSat': 'Job Satisfaction'}, inplace = False)

df.to_csv("processed_data.csv")