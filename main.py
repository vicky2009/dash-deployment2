import dash
from dash import html, dash_table, dcc
import weasyprint
from io import BytesIO
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import base64


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