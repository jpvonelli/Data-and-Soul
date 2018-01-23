import billboard

chart = billboard.ChartData('hot-100', date="1993-06-26")
#chart = billboard.ChartData('hot-100')()
outfile = open("hot-100-errors.txt", "a")

while chart.previousDate:
    chart = billboard.ChartData('hot-100', date=chart.previousDate)
    chartDate = str(chart.date)
    print(chartDate)

    if len(chart) == 0:
        outfile.write(chartDate + ": Chart data not found")
        outfile.write("\n")
        continue

    for rank in range(100):
        try:
            song = chart[rank]
        except Exception as ex:
            outfile.write(chartDate + ": Incomplete data")
            break
