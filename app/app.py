# -*- coding: utf-8 -*-
import dash as _dash
import dash_core_components as _dcc
import dash_html_components as _html
from dash.dependencies import Input, Output
from text import TextInvestigate
import plotly.graph_objs as _go
import nltk as _nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_nltk.download("stopwords")
_nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger")

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = _dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = _html.Div(
    children=[
        _html.Div(
            [
                _html.H1(children="Speech Sherlock \U0001F575"),
                _dcc.Input(id="input", placeholder="speech text", type="text"),
                _html.Div(
                    [_html.P(id="print-stats"), _html.P(id="print-text")]
                ),
            ]
        ),
        _html.Div(
            id="graph-container",
            children=[
                _dcc.Graph(id="graph"),
                _dcc.Slider(
                    id="num-words-slider",
                    min=5,
                    max=20,
                    value=15,
                    marks={str(val): str(val) for val in range(5, 30, 5)},
                    step=5,
                ),
            ],
        ),
        _dcc.Markdown(id="sentiment", style={"padding": 30, "fontSize": 30}),
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
        return f"Please enter speech ..."
    else:
        return f'Here is a preview: "{input_value[:500]} ..."'


@app.callback(
    Output(component_id="print-stats", component_property="children"),
    [Input(component_id="input", component_property="value")],
)
def update_output_stats_div(input):
    if not input:
        return ""
    else:
        return (
            f"You've entered a text of ",
            f"{TextInvestigate(input).get_raw_word_count()} words.",
        )


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

    word_counts = TextInvestigate(input).get_cleaned_word_counts()
    word_counts = word_counts[:num_words]
    word_counts_x = word_counts.values.tolist()
    word_counts_y = word_counts.index.tolist()

    return {
        "data": [_go.Bar(x=word_counts_x, y=word_counts_y, orientation="h")],
        "layout": _go.Layout(
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


@app.callback(
    Output(component_id="sentiment", component_property="children"),
    [Input(component_id="input", component_property="value")],
)
def analyze_sentiment(input):
    if not input:
        return ""
    else:
        analyser = SentimentIntensityAnalyzer()
        score = analyser.polarity_scores(input)

        max_score = sorted(
            score.items(), key=lambda item: item[1], reverse=True
        )[0]

        emoji_map = {
            "neg": "\U0001F641",
            "neu": "\U0001F610",
            "pos": "\U0001F603",
            "compound": "\U0001F937",
        }

        return "The main sentiment of the text is: " + emoji_map[max_score[0]]


if __name__ == "__main__":
    app.run_server(debug=True)

