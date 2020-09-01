from dotenv import load_dotenv
load_dotenv()

import os
import chevron
NOTION_V2_TOKEN = os.getenv("NOTION_V2_TOKEN")
BLOGMARKS_URL = "https://www.notion.so/380ce82124f74f959e25a03a31f696b4?v=5297dd0f955742128043cd769204ecfc"

from notion.client import NotionClient

client = NotionClient(token_v2=NOTION_V2_TOKEN)


# Get all blogmarks and sort by timestamp, most recent first.
cv = client.get_collection_view(BLOGMARKS_URL)

sort_params = [{
    "direction": "descending",
    "property": "created"
}]

result = cv.build_query(sort=sort_params).execute()

# Get public results because I'm struggling to get this filter working with the API
public = list(filter(lambda row: row.public == True, result))
# Convert to display dictionaries
top_five = list(map(lambda row: { "title": row.title, "url": row.url }, public[:5]))


with open('README.template.md', 'r') as f:
    file_content = chevron.render(f, { "blogmarks": top_five })

with open('README.md', 'w') as f:
    f.write(file_content)
    f.close

# Print the README.md
with open('README.md', 'r') as f:
    print(f.read())
