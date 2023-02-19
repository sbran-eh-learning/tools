#!/usr/bin/python3
import requests
from urllib.parse import urlparse

# Prompt the user for the URL to crawl
url = input("What address are we crawling: ")

# Extract the domain name from the original input URL
parsed_url = urlparse(url)
domain_name = parsed_url.netloc

# Initialize an empty list to keep track of all URLs found on the website
urllist = []

# Initialize an empty dictionary to keep track of which URLs have already been followed
isfollowed = {}

# This function checks if a given URL is in the list of URLs to crawl
def checkurllist(url):
    if url in urllist:
        return True
    else:
        return False

# This function checks if a given URL has already been followed
def isfollowedcheck(url):
    for entry in isfollowed.keys():
        if url != entry:
            return False
        else:
            if isfollowed[url] == "yes":
                return True
            else:
                return False

# Add the initial URL to the list of URLs to crawl
urllist.append(url)

# Loop through each URL in the list of URLs to crawl
for url in urllist:
    # Check if the URL has already been followed
    if isfollowedcheck(url) != True:
        # Send a GET request to the URL
        page = requests.get(url)
        # Mark the URL as followed
        isfollowed[url] = "yes"

        # Look for any links in the page source code
        start = "http"
        for line in page.text.split("\n"):
            if"http" in line:
                # Check if the line contains the same domain name as the original input URL
                if domain_name in line:
                    if "\">" in line:
                        end = "\">"
                    else:
                        end = "\" "
                    sliced = line[line.index(start):line.index(end)]
                    if "\"" in sliced:
                        end = "\""
                        parsedurl = sliced[sliced.index(start):sliced.index(end)]
                    else:
                        parsedurl = sliced
                    # Check if the parsed URL is already in the list of URLs to crawl
                    if checkurllist(parsedurl) == False:
                        # Add the parsed URL to the list of URLs to crawl
                        urllist.append(parsedurl)
                        # Mark the parsed URL as not yet followed
                        isfollowed[parsedurl] = "no"

# Print out all the URLs that were found on the website
for url in urllist:
    print(url)
