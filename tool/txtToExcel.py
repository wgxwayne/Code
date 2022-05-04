
import pandas as pd
import xlwt

df = pd.read_table('data.txt')
df.to_excel('data.xls', encoding='gbk')
