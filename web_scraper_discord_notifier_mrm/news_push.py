import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# Website URL
website_url = ''

# URL of the Discord webhook
webhook_url = ''

# Connect to sqlite database (or create it)
conn = sqlite3.connect('datesDB.sqlite')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Dates (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL UNIQUE
    )
''')
conn.commit()

# Requesting the website
r = requests.get(website_url)
r.raise_for_status()

# Parse the website
soup = BeautifulSoup(r.text, 'html.parser')

# Find all post cards
post_cards = soup.find_all(class_="elementor-post__card")

# Iterate over each post card
for card in post_cards:
    # Extract date and time
    date_element = card.find(class_="elementor-post-date")
    time_element = card.find(class_="elementor-post-time")

    # Get the date and time strings
    if date_element and time_element:
        current_date = date_element.text.strip()
        current_time = time_element.text.strip()

        # Combine date and time for uniqueness
        full_datetime = f"{current_date} {current_time}"

        # Check if this date has been processed before
        cursor.execute('SELECT date FROM Dates WHERE date = ?', (full_datetime,))
        data = cursor.fetchone()

        # If this date is new
        if data is None:
            # Extract title and excerpt
            title_element = card.find(class_="elementor-post__title")
            excerpt_element = card.find(class_="elementor-post__excerpt")
            read_more_element = card.find(class_="elementor-post__read-more-wrapper")

            title = title_element.text.strip()
            excerpt = excerpt_element.text.strip()
            read_more_link = read_more_element.find('a')['href']

            # Create message content
            content = f"[{title}](<{read_more_link}>)\n{excerpt}\n[Weiterlesen](<{read_more_link}>)"

            # Split content into chunks of 2000 characters
            messages = [content[i:i+2000] for i in range(0, len(content), 2000)]

            # Send each chunk as a separate message
            for message in messages:
                requests.post(webhook_url, json={"content": message})
                time.sleep(1)  # Delay for 1 second between messages to avoid rate limiting.

            # Add to database
            cursor.execute('INSERT INTO Dates (date) VALUES (?)', (full_datetime,))
            conn.commit()

# Close DB connection
conn.close()