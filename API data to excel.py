import openpyxl
import requests
import json

from datetime import date
from openpyxl.chart.axis import DateAxis

from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    ScatterChart,
    PieChart3D,
    Reference,
    Series,
   
)

#creating a virtual workbook
wb = openpyxl.Workbook()

#To activate the worksheet
sheet = wb.active

#data from an api to the workbook
url = 'https://api.coincap.io/v2/assets'
response = requests.get(url)

data = response.json()

for crypto in data["data"]:
    print(crypto["name"], crypto["symbol"], "- rank", crypto["rank"],
          "-maxSupply", crypto["maxSupply"])

rows = [
    ['Date', 'Batch 1', 'Batch 2', 'Batch 3'],
    [date(2015, 9, 1), 40, 30, 25],
    [date(2015, 9, 2), 40, 25, 30],
    [date(2015, 9, 3), 50, 30, 45],
    [date(2015, 9, 4), 30, 25, 40],
    [date(2015, 9, 5), 25, 35, 30],
    [date(2015, 9, 6), 20, 40, 35],
]

for row in rows:
    sheet.append(row)
#Chart Object
refObj = openpyxl.chart.Reference(sheet,
                                  min_col=1,
                                  min_row=1,
                                  max_col=1,
                                  max_row=10)

seriesObj = openpyxl.chart.Series(refObj, title='batch')

chartObj = openpyxl.chart.BarChart()

#LineChart
chartObj1 = LineChart()
chartObj1.title = "Date Axis"
chartObj1.style = 12
chartObj1.y_axis.title = "Size"
chartObj1.y_axis.crossAx = 500
chartObj1.x_axis = DateAxis(crossAx=100)
chartObj1.x_axis.number_format = 'd-mmm'
chartObj1.x_axis.majorTimeUnit = "days"
chartObj1.x_axis.title = "Date"
dates = Reference(sheet, min_col=1, min_row=2, max_row=7)
chartObj1.set_categories(dates)

chartObj1.title = 'My line chart'
chartObj1.append(seriesObj)

#Scatterchart
chartObj2 = ScatterChart()
chartObj2.title = "Scatter Chart"
chartObj2.style = 13
chartObj2.x_axis.title = 'date'
chartObj2.y_axis.title = 'Percentage'

xvalues = Reference(sheet, min_col=1, min_row=2, max_row=7)
for i in range(2, 4):
    values = Reference(sheet, min_col=i, min_row=1, max_row=7)
    series = Series(values, xvalues, title_from_data=True)
    chartObj2.series.append(series)

#Piechart
pie = PieChart3D()
labels = Reference(sheet, min_col=1, min_row=2, max_row=5)
data = Reference(sheet, min_col=2, min_row=1, max_row=5)
pie.add_data(data, titles_from_data=True)
pie.set_categories(labels)
pie.title = "My Pie"

chartObj.title = 'Barchart'
chartObj.append(seriesObj)

sheet.add_chart(chartObj, 'C2')
sheet.add_chart(chartObj1, 'L2')
sheet.add_chart(chartObj2, 'C20')
sheet.add_chart(pie, 'L20')

wb.save('DiffCharts.xlsx')
