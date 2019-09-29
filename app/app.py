# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from nltk.corpus import stopwords
import nltk
from text import tokenize, preprocess_words, get_word_counts
import plotly.graph_objs as go

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
stop_words = set(stopwords.words("english"))

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    children=[
        html.Div(
            [
                html.H1(children="Speech Sherlock"),
                dcc.Input(id="input", placeholder="speech text", type="text"),
                html.Div(id="print-text"),
            ]
        ),
        html.Div(
            id="graph-container",
            children=[
                dcc.Graph(id="graph"),
                dcc.Slider(
                    id="num-words-slider",
                    min=5,
                    max=20,
                    value=15,
                    marks={str(val): str(val) for val in range(5, 30, 5)},
                    step=5,
                ),
            ],
        ),
    ]
)


@app.callback(Output("graph-container", "style"), [Input("input", "value")])
def hide_graph(input):
    """Only show graph if there is data."""
    if input:
        return {"display": "block"}
    else:
        return {"display": "none"}


@app.callback(
    Output(component_id="print-text", component_property="children"),
    [Input(component_id="input", component_property="value")],
)
def update_output_div(input_value):
    if not input_value:
        return f"Please enter speech"
    else:
        return f'You\'ve entered "{input_value}"'


@app.callback(
    Output(component_id="graph", component_property="figure"),
    [
        Input(component_id="input", component_property="value"),
        Input("num-words-slider", "value"),
    ],
)
def analyze_text(input, num_words):
    if input is None:
        return {}

    tokenized_words = tokenize(input)
    # TODO: pass stopwords differently
    preprocessed_words = preprocess_words(tokenized_words, stop_words)
    word_counts = get_word_counts(preprocessed_words, stop_words)
    word_counts = word_counts[:num_words]
    word_counts_x = word_counts.values.tolist()
    word_counts_y = word_counts.index.tolist()

    return {
        "data": [go.Bar(x=word_counts_x, y=word_counts_y, orientation="h")],
        "layout": go.Layout(
            yaxis=dict(
                autorange="reversed", title="words used", automargin=True
            ),
            xaxis=dict(
                automargin=True,
                title="number of times used",
                showgrid=False,
                showline=True,
                tickformat=",d",
            ),
        ),
    }


if __name__ == "__main__":
    app.run_server(debug=True)

