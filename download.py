import json
import os

import requests


# Recursively download all child pages and save each page in its own file
def download_pages(page_id, parent_path=""):
    # Get the page content
    page_url = f"{base_url}/rest/api/content/{page_id}?expand=body.view,version,children.page"
    response = session.get(page_url)

    # Parse the JSON response and get the page title and content
    page = json.loads(response.text)
    title = page["title"]
    content = page["body"]["view"]["value"]

    # Create a new file with the page title as the filename and save the content to it
    path = os.path.join(parent_path, title)
    filename = f"{path}.html"
    # create the directory path if it doesn't exist
    directory = os.path.dirname(filename)
    print(f"{filename} {directory}")
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Page {title} saved to {filename}")

    # Recursively download all child pages
    if "children" in page:
        children = page["children"]["page"]["results"]
        for child in children:
            child_id = child["id"]
            download_pages(child_id, path)


if __name__ == "__main__":
    # Enter the base URL of your Confluence instance and the space key of the space you want to download
    base_url = "https://cwiki.apache.org/confluence/"
    space_key = "BEAM"

    # Enter your Confluence username and password or an API token
    username = "<USER_NAME>"
    password = "<PASSWORD>"

    # Create a session object and set the username and password or API token
    session = requests.Session()
    session.auth = (username, password)

    # Get the list of all pages in the space
    url = f"{base_url}/rest/api/content?spaceKey={space_key}&type=page"
    response = session.get(url)

    # Parse the JSON response and get the list of page IDs
    pages = json.loads(response.text)["results"]
    page_ids = [page["id"] for page in pages]

    # set the path of the output directory
    parent_path = "Apache Beam Documentation/"

    # Loop through the page IDs and download each page and its child pages
    for page_id in page_ids:
        download_pages(page_id, parent_path=parent_path)
