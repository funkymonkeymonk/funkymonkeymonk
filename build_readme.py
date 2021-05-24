import sys

from dotenv import load_dotenv
load_dotenv()

import os
import chevron
import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def main(NOTION_TOKEN):
    blogmarks = get_blogmarks(NOTION_TOKEN)
    print(blogmarks)
    readme_content = prepare_readme(blogmarks)
    print(readme_content)
    write_and_print('README.md', readme_content)

def get_blogmarks(NOTION_TOKEN):
    data = {
        "filter": {
            "property": "Public",
            "checkbox": {
                "equals": True
            }
        },
        "sorts": [
            {"property": "Date", "direction": "descending"},
            {"property": "Name", "direction": "ascending"}
        ],
        "page_size": 5
    }

    res = requests.post("https://api.notion.com/v1/databases/3cbc9526987c4b8bbe26d1b1a968c62b/query", auth=BearerAuth(NOTION_TOKEN), json=data)

    if res.status_code != 200:
        print("Request to Notion failed with status: " + str(res.status_code))
        sys.exit(1)

    raw = res.json()['results']
    blogmarks = { "blogmarks": list(map(lambda row: { "title": row['properties']['Name']['title'][0]['plain_text'], "url": row['properties']['URL']['url'] }, raw)) }
    return blogmarks

def get_public(result):
    return list(filter(lambda row: row.public == True, result))

def prepare_readme(blogmarks):
    with open('README.template.md', 'r') as f:
        file_content = chevron.render(f, blogmarks)
    return file_content

def write_and_print(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content)
        f.close()

    with open(file_name, 'r') as f:
        print(f.read())
        f.close()

if __name__ == "__main__":
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    if (NOTION_TOKEN):
        main(NOTION_TOKEN)
    else:
        print('Failed to get NOTION_TOKEN from the environment')
        exit(1)
