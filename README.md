# SupervisionHack_picipolo

Organised by the Polish Financial Supervision Authority. 

## The task was to prepare data from PDF files, which we had to scrape from portals provided by the organizers.

### The main goals were to create 5 csv tables containing:
- meta data information about the pdf
- bag of words (non-standardized)
- bag of words (normalized - stemming, lemmatization)
- checking if the pdf has the given expressions
- extraction of most important data

## Setup
You can setup your own environment using our `requirements.txt` file. We recommend using `conda` and command: `conda create --name <env> --file requirements.txt`

To download all pdfs required for validation you can use our scrapper, by running python3 `main.py` located in `/scraper`.

If you want to use your own pdfs, insert them in `/results` directory.

In order to validate pdfs located in `/results` directory, run `python3 main.py`

## Future implementation
We plan to extend our application by adding advanced deep learning modules & gui, which prototype is included in our PRs. It was created in `streamlit`, however it can be extended in `React.js`

### Authors:
- Mikołaj Gałkowski
- Hubert Bujakowski
- Maja Andrzejczuk
- Łukasz Tomaszewski
- Wiktor Jakubowski
