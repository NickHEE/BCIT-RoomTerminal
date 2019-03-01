import pandas as pd
import lxml

url = 'https://studyrooms.lib.bcit.ca/day.php?year=2019&month=2&day=27&area=4'
table = pd.read_html(url, attrs={'id':'day_main'})
print(table)
