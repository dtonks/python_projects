import pandas as pd


def create_list(filename):
  df = pd.read_excel(filename) # can also index sheet by name or fetch all sheets
  mylist = df['TailNumber'].tolist()
  return mylist

print("Input location and filename:\n")
filename = input(str(""))
print(create_list(filename))
