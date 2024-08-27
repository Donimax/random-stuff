import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import re

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

# Find the first entry in the news section
news_section = soup.find(class_="news")
entry_element = news_section.find(class_="entry") if news_section else None

# Function to convert HTML text to Discord markdown
def convert_to_discord_markdown(html_text):
    """
    Converts simple HTML tags into Discord-flavored markdown.
    """
    transformations = {
        '<div class="text">': '',
        '</div>': '',
        '<b>': '**',
        '</b>': '** ',
        '<i>': '*',
        '</i>': '*',
        '<u>': '__',
        '</u>': '__',
        '<s>': '~~',
        '</s>': '~~',
        '<p>': '',
        '</p>': '\n',
        '<h1>': '***',
        '</h1>': '** *\n',
        '<h2>': '**',
        '</h2>': '** \n',
        '<h3>': '**',
        '</h3>': '** \n',
        '<h4>': '**',
        '</h4>': '** \n',
        '<h5>': '**',
        '</h5>': '** \n',
        '<h6>': '**',
        '</h6>': '** \n',
        '<blockquote>': '> ',
        '</blockquote>': '\n',
        '<pre>': '```\n',
        '</pre>': '```\n',
        '<code>': '`',
        '</code>': '`',
        '<br>': '\n',
        '<hr>': '---\n',
    }

    # Replace simple tags
    for html_tag, markdown in transformations.items():
        html_text = html_text.replace(html_tag, markdown)

    # Transform links
    soup = BeautifulSoup(html_text, 'html.parser')
    for a_tag in soup.find_all('a', href=True):
        link_text = a_tag.text.strip()
        link_href = a_tag['href']
        markdown_link = f'[{link_text}]({link_href})'
        a_tag.replace_with(markdown_link)

    return str(soup)

if entry_element:
    # Find the date within the entry
    date_element = entry_element.find(class_="date")

    # Check if the date exists and non-empty
    if date_element and date_element.text.strip():
        current_date = date_element.text.strip()

        # Check if this date has been processed before
        cursor.execute('SELECT date FROM Dates WHERE date = ?', (current_date,))
        data = cursor.fetchone()

        # If this date is new
        if data is None:
            # Add to database
            cursor.execute('INSERT INTO Dates (date) VALUES (?)', (current_date,))
            conn.commit()

            # Find text within the entry
            text_element = entry_element.find(class_="text")
            if text_element:
                # Get HTML text and convert to Discord markdown
                content = convert_to_discord_markdown(str(text_element))
                
                # Append current date to the content
                content = f'{current_date}\n{content}'
                
                # Split content into chunks of 2000 characters
                messages = [content[i:i+2000] for i in range(0, len(content), 2000)]

                # Send each chunk as a separate message
                for message in messages:
                    requests.post(webhook_url, json={"content": message})
                    time.sleep(1) # Delay for 1 second between messages. To avoid rate limiting.

# Close DB connection
conn.close()
