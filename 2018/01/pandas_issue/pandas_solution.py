# this is an example of the code I have but it isn't working properly
from datetime import datetime
import pandas as pd

input_filename = 'input.csv'
output_filename = 'output.csv'

timenow = datetime.now()




# reads dataframe from example.csv
historical_df = pd.read_csv(input_filename)
historical_df.set_index('timestamp', inplace=True)

# gets new data from API ### 1st API call
new_data = pd.DataFrame([timenow, 22313, 14699.88, 18.7]).T
new_data.columns = ['timestamp', 'col 4', 'col 5', 'col 6']

new_data.set_index('timestamp', inplace=True)

# Concat current data to historical DF and dump to excel
historical_df = historical_df.combine_first(new_data)

# Save to CSV
historical_df.to_csv(output_filename)




### 2nd API call with the same time
# reads dataframe from example.csv
historical_df = pd.read_csv(output_filename)
historical_df.set_index('timestamp', inplace=True)

# gets new data from API
new_data = pd.DataFrame([timenow, 3589, 2385.74, 17.6405]).T
new_data.columns = ['timestamp', 'col 1', 'col 2', 'col 3']

new_data.set_index('timestamp', inplace=True)

# Concat current data to historical DF and dump to excel
historical_df = historical_df.combine_first(new_data)

# Save to CSV
historical_df.to_csv(output_filename)
