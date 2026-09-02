import pandas as pd

from test_read import extract_data
from transform import transform_data


df = extract_data()

print("Before transformation:")
print(df.shape)

df = transform_data(df)

print("\nAfter transformation:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nSample:")
print(df.head())