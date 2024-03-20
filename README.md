# UpCode
A software for uploading all your accepted solutions from CodeForces, and Atcoder, CodeChef(Currently under Beta testing) to Github with no hassles, and fully automated using Python (Selenium and Chrome drivers).

## How to use:
* Generate an API key from https://github.com/settings/tokens. Make sure the repo section is checked.
* Run the following command in terminal:

  ```
  pip install -r requirements.txt
  ```
* To start using the project, run the following command in terminal:

  ```
  python3 main.py
  ```

### Modules used:
* `requests` and `grequests` to get the html
* BeautifulSoup4 (`bs4`) to parse the html
* `selenium` to make CodeForces scraper more reliable
* `webdriver_manager` to automatically create the chromium executable
* `PyGithub` to access the GitHub API
* `json` to parse CodeForces API
* `multiprocessing` to parallelize CodeForces and CodeChef uploads
* Misc: `time`, `logging`, `dotenv`, `inspect`
