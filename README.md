# Immo Eliza - Data Scraper

A group project @ [BeCode.org](https://becode.org/) as part of the **AI Bootcamp** in Gent

## Project description

This is the first stage of a larger project to create a Machine Learning (ML) model to predict sell prices of real estate properties in Belgium.

The current task is to gather actual data (at least 10,000 entries) from the Belgian real estate market. This data will be used to train and test ML prediction model.

The dataset delivered as a `csv` file and covers the following subjects:

- ID number
- Source URL
- Price
- Property type
- Locality and address (if available)
- Number of bedrooms
- Livable surface
- Building information (construction year, facade count, floor count, etc.)
- Property condition
- Kitchen type
- Garden and its surface (if any)
- Terace and its surface (if any)
- The surface of land (for houses)
- Availability of some extras:
  - Open fire
  - Swimming pool
  - Airconditioner
- Available facilities:
  - Number of bathrooms, showers, and/or toilets
  - Number of parking spaces
- Energy consumption information
- Sale type

The Python-based tool uses [ImmoWeb](https://www.immoweb.be/en) website, the leading real estate website in Belgium, to scrape the required information and stores it in a dictionary format and later is written as a `csv` file.

## Installation

1. Clone the [immoweb-scraper](https://github.com/feldeh/immoweb-scraper) repository
2. Navigate to the root of the repository
3. Install the required libraries by running `pip install -r requirements.txt`

## Usage

- Execute the script by running the command `python main.py` in the terminal.
- This will scrape the property listing informations from [ImmoWeb](https://www.immoweb.be/en) and store them in the `data` directory in both `json` and `csv` formats.

## Timeline

This stage of the project lasted 4 days in the week of June 26-30, 2023.

## The Team

The project was made by a group of Junior AI & Data Scientists (in alphabetical order):

- Félicien De Hertogh [LinkedIn](https://www.linkedin.com/in/feliciendehertogh/) | [GitHub](https://github.com/feldeh)
- César E. Mendoza V. [LinkedIn](https://www.linkedin.com/in/mendoce24/) | [GitHub](https://github.com/mendoce24)
- Mykola Senko [LinkedIn](https://www.linkedin.com/in/mykola-senko-683510a4/) | [GitHub](https://github.com/MykolaSenko)
- Vitaly Shalem [LinkedIn](https://www.linkedin.com/in/vitaly-shalem-26aab265/) | [GitHub](https://github.com/vitaly-shalem)

## Instruction

The project was completed under the supervision of [Vanessa Rivera Quiñones](https://www.linkedin.com/in/vriveraq/) and [Samuel Borms](https://www.linkedin.com/in/sam-borms/?originalSubdomain=be)

Gent | June 30, 2021
