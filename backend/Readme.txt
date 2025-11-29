# Web Scraping with Python

## Description
This project demonstrates a basic web scraping workflow using Python.  
It uses the `requests` library to fetch web pages and can be extended 
to parse and process data from websites.

---

## Requirements
- Python 3.13 or higher  
- pip (Python package manager)  
- `requests` library  

Optional:  
- `BeautifulSoup` (`bs4`) for HTML parsing if you plan to process HTML content.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>

2. Create a virtual environment (recommended)
python -m venv .venv

3. Activate the virtual environment
PowerShell (Windows)
.venv\Scripts\Activate.ps1

Linux
source .venv/bin/activate

Command Prompt (Windows)
.venv\Scripts\activate


If you get an execution policy error, run:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

Command Prompt (Windows)
.venv\Scripts\activate

4. Install required packages
pip install -r requirements.txt

Run the main script:

python fetch_requests.py

To recreate the environment later:
python -m venv .venv
.venv\Scripts\Activate.ps1
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt


Wordpress Credentials
------------------------
http://localhost:8080/myvideosite/wp-login.php
Admin
Admin@1312


For WP Backup & Migrations
https://wordpress.org/plugins/updraftplus/
Download the ZIP file.
On your computer, unzip the file (optional — depends on method).
Using File Explorer, go to:
D:/xampp/htdocs/myvideosite/wp-content/plugins/
Copy the updraftplus plugin folder into this plugins directory.
Go to your WordPress Dashboard → Plugins → Installed Plugins → you should now see “UpdraftPlus” → click Activate.