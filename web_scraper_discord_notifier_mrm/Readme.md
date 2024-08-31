# Web Scraper & Discord Notifier

This script scrapes a website for updates, and if a new update is found, it sends the update to a Discord webhook. The script runs every 30 minutes using a cron job.

## Requirements

The script is written in Python 3 and requires the following Python packages:
- `requests`
- `beautifulsoup4`
- `sqlite3` (included in Python's standard library)

## Installation on Ubuntu/Debian

1. **Update your system:** 

    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2. **Install Python3 and pip (if not already installed):** 

    ```bash
    sudo apt install python3 python3-pip -y
    ```

3. **Install required Python packages:** 

    ```bash
    sudo apt install python3-requests python3-bs4 -y
    ```

4. **Clone the repository:** 

    ```bash
    git clone https://github.com/Donimax/random-stuff.git
    cd random-stuff/web_scraper_discord_notifier_mrm
    ```

5. **Configure the script:** 

    - Open the script in a text editor:

        ```bash
        vim news_push.py
        ```

    - Set the `website_url` and `webhook_url` variables to the desired website and Discord webhook.

    - Save and exit the editor.

6. **Set up a cron job to run the script every 30 minutes:** 

    - Open the crontab file:

        ```bash
        crontab -e
        ```

    - Add the following line to run the script every 30 minutes:

        ```bash
        */30 * * * * /usr/bin/python3 /path/to/your/news_push.py
        ```

    - Save and exit the crontab editor.

## Usage

The script will automatically run every 30 minutes and check for updates on the specified website. If a new update is found, it will be sent to the configured Discord webhook.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
