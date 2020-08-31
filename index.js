require('dotenv').config();
const Notion = require("notion-api-js").default;

const notion = new Notion({
  token: process.env.NOTION_TOKEN
});

notion.getPages().then(pages => {
    console.log(pages);
  });