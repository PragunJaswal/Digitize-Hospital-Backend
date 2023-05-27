import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSJ-NPTPsvgZLaBT1S18hTIiZZa_zkAs6qiYzg-BILvn35hiPEeXAJToLEVYHWu9Bt3k6mJvx5jmJs_/pubhtml'

print("started")
df = pd.read_html(url)[0]  # read the first (and only) table from the HTML
df.to_csv('data.csv', index=False)  # save the DataFrame to a CSV file
print("done")