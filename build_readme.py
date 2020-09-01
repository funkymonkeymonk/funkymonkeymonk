from dotenv import load_dotenv
load_dotenv()

import os
import chevron
from notion.client import NotionClient

NOTION_V2_TOKEN = os.getenv("NOTION_V2_TOKEN")
BLOGMARKS_URL = "https://www.notion.so/380ce82124f74f959e25a03a31f696b4?v=5297dd0f955742128043cd769204ecfc"

def main(notion_client):
    result = getAllBlogmarks(notion_client)
    public = get_public(result)
    readme_content = prepare_readme(public)
    write_and_print('README.md', readme_content)

def getAllBlogmarks(client):
    cv = client.get_collection_view(BLOGMARKS_URL)

    sort_params = [{
        "direction": "descending",
        "property": "created"
    }]
    
    return cv.build_query(sort=sort_params).execute()

def get_public(result):
    return list(filter(lambda row: row.public == True, result))

def prepare_readme(public):
    most_recent = public[:5]
    blogmarks = { "blogmarks": list(map(lambda row: { "title": row.title, "url": row.url }, most_recent)) }
    with open('README.template.md', 'r') as f:
        file_content = chevron.render(f, blogmarks)
    return file_content

def write_and_print(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content)
        f.close

    with open(file_name, 'r') as f:
        print(f.read())
        f.close

notion_client = NotionClient(token_v2=NOTION_V2_TOKEN)
main(notion_client)