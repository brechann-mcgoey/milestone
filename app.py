import quandl
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure
from bokeh.embed import components


from flask import Flask, render_template, request, redirect

app = Flask(__name__)

quandl.ApiConfig.api_key=os.environ["qandl_key"]

def create_figure(ticker_name):
    enddate=datetime.today().strftime("%Y-%m-%d")
    startdate=(datetime.today()-relativedelta(months=1)).strftime("%Y-%m-%d")
    data = quandl.get("WIKI/"+ticker_name, start_date=startdate, end_date=enddate,column_index=4)
    data=data.reset_index()

    # prepare some data
    x = data["Date"]
    y = data["Close"]

    # output to static HTML file
    #output_file("lines.html")

    # create a new plot with a title and axis labels
    p = figure(title=ticker_name, x_axis_label='Date', y_axis_label='Closing price',x_axis_type='datetime')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Closing price", line_width=2)

    return p


@app.route('/')
def index():
    plot=create_figure("GOOGL")
    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template('index.html', script=script, div=div)



if __name__ == '__main__':
    #app.run(port=33507)
    app.run(host='0.0.0.0',port=33507)
