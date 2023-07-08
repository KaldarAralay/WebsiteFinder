# Web Crawler

This Python script is a basic web crawler that traverses and visits URLs starting from a set of initial URLs.

## How it works

The script uses the BeautifulSoup library to parse the HTML of the visited pages and find all the links. It then adds these links to a queue of URLs to visit next. The script is designed to respect the robots.txt files of the websites it visits, ensuring it only accesses pages it's allowed to.

The script uses multiprocessing to visit multiple URLs in parallel, speeding up the crawling process. The URLs visited by the crawler are stored in a file for record-keeping.

## Usage

Run the script by using the command: `python finder.py`. The script will start the crawling process from two hardcoded URLs ("https://www.site1.com/" and "https://www.site2.com/"). 

Make sure to install all the required dependencies before running the script. The dependencies are listed in the `requirements.txt` file and can be installed using pip: `pip install -r requirements.txt`.

**Note:** This script writes the URLs it visits to two separate files: `paths.txt` and `no_paths.txt`. If the URL has a path, it's written to `paths.txt`, otherwise it's written to `no_paths.txt`.
