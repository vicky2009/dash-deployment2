# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

'''
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
import weasyprint
from io import BytesIO
import base64

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import base64
import plotly.graph_objects as go
import dash_table

from plotly.io import to_image

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div([
    html.H1('Hello Dash'),

    dcc.Graph(id='example-graph', figure=fig),

    html.Div([
        html.H2('Table'),
        html.Div(
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records')
            ),
            style={
                'maxHeight': '300px',
                'overflowY': 'scroll'
            }
        )
    ]),

    html.Button('Download PDF', id='download-pdf'),

    html.Div(id='pdf-content')
])


@app.callback(
    dash.dependencies.Output('pdf-content', 'children'),
    dash.dependencies.Input('download-pdf', 'n_clicks'),
    State('table', 'data')
)
def generate_pdf(n_clicks, table_data):
    if n_clicks:
        # create a WeasyPrint PDF object from the HTML content
        # Create HTML content with table and graph
        df2 = pd.DataFrame(table_data)
        table_html = df2.to_html(classes='table')

        html_content = '<h2>Hello world</h2>' f'<div>{table_html}</div>'
        pdf_file = BytesIO()
        weasyprint.HTML(string=html_content).write_pdf(pdf_file)

        # set up the anchor tag to download the PDF file
        return html.A('Download PDF',
                      href='data:application/pdf;base64,' + base64.b64encode(pdf_file.getvalue()).decode(),
                      download='example.pdf')

    return ''


if __name__ == '__main__':
    app.run_server(debug=False, port=8062)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
