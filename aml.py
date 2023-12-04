import pandas as pd

# DataFrame 
pd.set_option('display.max_rows', None)
data = pd.read_excel('/Users/jameswyse/Desktop/Work/Interviews/Peregrine/AML_exercise_dataset.xlsx')
df = pd.DataFrame(data)

# Describe dataframe
describe = df.describe()

# Set DataFrame Index
df = df.set_index('Unnamed: 0')

# Convert DataFrame date columns to datetimes
df['Send DateTime'] = pd.to_datetime(df['Send DateTime'])
df['Pay DateTime'] = pd.to_datetime(df['Pay DateTime'])

# Isolate transaction amounts column and get std, mean
amount = df['Amount'].astype(float)
std_deviation = amount.std()
mean = amount.mean()

# Filter dataframe by mean + 1 std_deviation
df = df.loc[(amount > (mean + std_deviation))]

# Get all time differences for transactions between "sent" and "received" dates
time_difference = abs(df['Send DateTime'] - df['Pay DateTime'])

# Filter dataframe where the transaction times sent and received are within 24 hrs
df = df.loc[(time_difference < pd.Timedelta('24 hours'))]

# Generate new dataframe by getting total count of txns sent by individuals
total_txns = df['Sender Name_'].value_counts()

# Filter the total_txns dataframe even further by only selecting individuals with > 5 txns
frequent_txns = total_txns.loc[(total_txns > 5)]

# Merge the original dataframe and the new filtered dataframe to narrow down potential suspects
df_merge = pd.merge(df, frequent_txns, left_on="Sender Name_", right_on="Sender Name_")

