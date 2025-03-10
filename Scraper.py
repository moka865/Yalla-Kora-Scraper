import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv
import time
import random
import os
# Headers to simulate a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def fetch_page(date, retries=3):
    """Fetches the match page based on the given date with retry logic."""
    url = f'https://www.yallakora.com/match-center/?date={date}#days'
    
    for attempt in range(retries):
        try:
            with requests.Session() as session:
                response = session.get(url, headers=HEADERS, timeout=10)
                response.raise_for_status()  # Raise an error for failed responses
            return response.content
        except requests.RequestException as e:
            print(f"Error fetching data for {date}: {e}")
            if attempt < retries - 1:
                wait_time = random.uniform(0, 1)  # Add a random delay before retrying
                print(f"Retrying in {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                print("Maximum retries reached. Skipping this date.")
                return None



def scrape_matches(html_content, match_date):
    """Parses the page and extracts match details."""
    soup = BeautifulSoup(html_content, 'lxml')
    championships = soup.find_all('div', class_='matchCard')

    all_matches = []
    for championship in championships:
        all_matches.extend(extract_match_info(championship, match_date))  
    
    return all_matches

def extract_match_info(championship, match_date):
    """Extracts match details from a championship section."""
    match_info = []
    championship_name = championship.find('h2').text.strip()
    matches = championship.find_all('div', class_='liItem')

    for match in matches:
        try:
            team_a = match.find('li', class_='ScoreCell__Item--home').find('div', class_='ScoreCell__TeamName').text.strip()
            team_b = match.find('li', class_='ScoreCell__Item--away').find('div', class_='ScoreCell__TeamName').text.strip()

            scores = match.find('div', class_='MResult').find_all('span', class_='score')
            score = " - ".join(s.text.strip() for s in scores) if scores else "Not played yet"

            match_time = match.find('div', class_='MResult').find('span', class_='time')
            match_time = match_time.text.strip() if match_time else "Not available"

            match_info.append({
                'Match Date': match_date,
                'Championship': championship_name,
                'Team A': team_a,
                'Team B': team_b,
                'Score': score,
                'Time': match_time
            })
        except AttributeError:
            print(f"Could not extract match data in {championship_name}")
    
    return match_info














def save_to_csv(matches, filename='Matches.csv'):
    """Saves match data to a CSV file."""
    if not matches:
        print("No matches found to save.")
        return

    keys = matches[0].keys()
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(matches)
        print(f'Data saved to {filename}')
    except IOError as e:
        print(f"Error saving data: {e}")

def fetch_single_day():
    """Fetch matches for a single day."""
    date = input("Enter the date (MM/DD/YYYY): ")
    html_content = fetch_page(date)
    
    if html_content:
        matches = scrape_matches(html_content, date)
        save_to_csv(matches)

def fetch_date_range():
    """Fetch matches for a range of dates."""
    start_date = input("Enter start date (MM/DD/YYYY): ")
    end_date = input("Enter end date (MM/DD/YYYY): ")

    start_date = datetime.strptime(start_date, "%m/%d/%Y")
    end_date = datetime.strptime(end_date, "%m/%d/%Y")

    all_matches = []
    current_date = start_date

    while current_date <= end_date:
        formatted_date = current_date.strftime("%m/%d/%Y")
        print(f"Fetching data for {formatted_date}...")

        html_content = fetch_page(formatted_date)
        if html_content:
            matches = scrape_matches(html_content, formatted_date)
            all_matches.extend(matches)

        wait_time = random.uniform(0, 1)
        print(f"Waiting {wait_time:.2f} seconds before the next request...")
        time.sleep(wait_time)

        current_date += timedelta(days=1)

    save_to_csv(all_matches)

def main():
    """Main function to let the user choose an option."""
    print("\nYalla Kora Match Scraper")
    print("1. Fetch matches for a single day")
    print("2. Fetch matches for a date range")
    
    choice = input("\nChoose an option (1 or 2): ").strip()

    if choice == "1":
        fetch_single_day()
    elif choice == "2":
        fetch_date_range()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()