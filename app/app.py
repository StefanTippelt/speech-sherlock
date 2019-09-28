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
    [
        html.H1(children="Speech Sherlock"),
        dcc.Input(id="input-field", placeholder="speech text", type="text"),
        html.Div(id="print-text"),
        html.Div(id="processed-text"),
        dcc.Graph(
            id="counting-graph",
            figure={
                "data": [
                    {
                        "y": [4, 1, 2],
                        "x": [1, 2, 3],
                        "type": "bar",
                        "name": "SF",
                    },
                    {
                        "x": [1, 2, 3],
                        "y": [2, 4, 5],
                        "type": "bar",
                        "name": "Montréal",
                    },
                ],
                "layout": {"title": "Dash Data Visualization"},
            },
        ),
    ]
)


@app.callback(
    Output(component_id="print-text", component_property="children"),
    [Input(component_id="input-field", component_property="value")],
)
def update_output_div(input_value):
    if not input_value:
        return f"Please enter speech"
    else:
        return f'You\'ve entered "{input_value}"'


@app.callback(
    Output(component_id="processed-text", component_property="children"),
    [Input(component_id="input-field", component_property="value")],
)
def analyze_text(input_value):
    tokenized_words = tokenize(input_value)
    # TODO: pass stopwords differently
    preprocessed_words = preprocess_words(tokenized_words, stop_words)
    word_counts = get_word_counts(preprocessed_words, stop_words)
    print(word_counts)
    return word_counts


if __name__ == "__main__":
    app.run_server(debug=True)

