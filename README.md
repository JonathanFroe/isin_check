# ISIN-Check ![GitHub all releases](https://img.shields.io/github/downloads/JonathanFroe/isin_check/total?color=green&logo=Github)

<img src="assets/Logo.png" alt="ISIN-Check Logo" width="100">

## Automated Stock and ETF Data Retrieval, Sorting, and Export Tool

---
ISIN-Check is a powerful tool designed to automate the process of downloading the latest information about stocks or ETFs using their International Securities Identification Number (ISIN). With its efficient functionality, it enables users to effortlessly retrieve, sort, and export the data into an Excel file for further analysis and tracking.

## Key Features

- **Automated Data Retrieval**: ISIN-Check automates the process of fetching the most up-to-date information about stocks or ETFs using their ISIN. Save time and effort by eliminating manual data collection.

- **Extensive Coverage**: Our tool provides comprehensive coverage of stocks and ETFs across various markets and exchanges, allowing you to access a wide range of investment options.

- **Sorting**: ISIN-Check empowers you to sort  the retrieved data based on key parameters such as ISIN, WKN, performance, volatility, and more. Focus on the specific information that is relevant to your investment strategy.

- **User-Friendly Interface**: ISIN-Check features a user-friendly interface that makes navigating the tool intuitive and straightforward. Easily access and utilize its powerful features, whether you're a novice or an experienced investor.

- **Excel Export**: Effortlessly export the sorted and filtered data into an Excel file. Conduct further analysis, track your investments, and integrate the data with other financial tools as needed.


## Usage

To use ISIN-Check Tool, follow these two easy steps:

1. Download the .exe file: [Latest release here (v0.2.0)](https://github.com/JonathanFroe/isin_check/releases/tag/v.0.2.0)

2. Run it!

## New features for v0.2.0

- **Enhanced Multithreading Support**: Latest update incorporates advanced multithreading techniques to significantly accelerate the data retrieval process. Own tests have demonstrated an impressive _**9x**_ increase in speed.
- **Added WKN Column**: Now the Table also shows the representative WKN-Nummber of each ISIN.
- **Added second and third Tag-Column**: Now instead of only one Tag Column, you have 3 possible Tag-Columns to sort and organize.
- **Double-Click to Copy**: Double-click on a cell will copy the text into the clipboard.
- **Descending Sorting**: By clicking again, it will now sort the other way around. Very useful if you want to sort the Best-Performing first.

## Bugfixes for v0.2.0
- **Solved: Tags not saved**: Tags are now saved to the database after updating them.
- **Solved: Overriding old database**: Old or other database can now be loaded into the program without overriding them with the current one.

*Please report all bugs via an issue request!*

## Troubleshooting
- *Program crashes every time I try to start it*: 
Try deleting the config-isincheck.conf file and start the program again.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.


**Note:** ISIN-Check does not provide financial advice or recommendations. Always consult with a qualified financial advisor before making investment decisions.
