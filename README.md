# Yalla-Kora-Scraper
Yalla Kora Match Scraper is a Python-based tool that fetches football match details from the Yalla Kora website for a specified date or date range. The program extracts key information, including team names, match time, tournament name, and match results (if available). The retrieved data is then stored in a structured CSV file for further analysis or reference.

 Features
 Fetches match data for a single day or a date range.
 Extracts details like teams, match time, tournament name, and score.
 Implements retry logic to handle network issues gracefully.
 Introduces random delays to mimic human behavior and avoid request blocking.
 Saves the extracted data in a well-structured CSV file for easy access.

⚙ Technologies Used

Python (Core programming language)
Requests (For making HTTP requests)
BeautifulSoup (For parsing and extracting match data from HTML)
CSV Module (For storing data in CSV format)
Datetime & Time (For handling date inputs and delays)
Random (For introducing variable delays between requests)
 How It Works

Choose an option: Fetch matches for a single day or a date range.
Enter the date(s) in MM/DD/YYYY format.
The program fetches match details from Yalla Kora.
Extracted data is saved automatically in a CSV file.
