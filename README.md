# Speech Sherlock :male_detective:	

A simple web app for natural language processing and counting of most frequent words used.
The tool is meant for quick exploration of texts like puplic speeches.
The app is based on [Dash](https://github.com/plotly/dash) and is using natural language toolkit [nltk](https://github.com/nltk/nltk).

## How it works
Insert any text in the input field and get a chart with most frequent words used. Use the slider for showing the amount of words you are interested in.

![App Overview](images/overview.jpg)

Additionally there is a sentiment analysis performed based on [NLTK VADER](https://www.nltk.org/_modules/nltk/sentiment/vader.html) sentiment analysis. The output is mapped to emojis and show the most important sentiment of the text.

![App Overview](images/sentiment.jpg)


Some sample data for exloration of the tool can be found in `data/`

[source for speeches](https://www.fridaysforfuture.org/greta-speeches)



## Installation
For installation of the project please run
```
$ make deps
```

## Run the app
To start the app, run
```
$ make run
```

## Go to browser to view the app
```
http://localhost:8050/
```

## Licence
MIT
