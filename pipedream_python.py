import requests
from notion_client import Client
import json
import re
from pocket import Pocket

def handler(pd: "pipedream"):#extract url from pocket.json
  def url():
    extracted_url = pd.steps["trigger"]["event"]["given_url"]
    return extracted_url
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  def name():#extract name from pocket.json
    name = pd.steps["trigger"]["event"]["resolved_title"]
    name = re.sub(r'\#\w+', '', name)
    name = name[:100]
    return name
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  def get_tags():#extract tags from pocket api call because pipedreams call doesn't return tags because of detailType not being "complete"
    consumer_key = "your-consumer-key"
    access_token = "your-access-token"
    pocket_instance = Pocket(consumer_key, access_token=access_token)
    response = pocket_instance.get(detailType="complete")
    new_tuple = response[:1]

    for e in new_tuple[0]["list"]:
        if e == pd.steps["trigger"]["event"]["item_id"]:
            tags = new_tuple[0]["list"][e]["tags"]
            tags_list = [{"name": tag} for tag in tags]
            return tags_list
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  def db_id_set(extracted_url):#set database id depending on type of saved content
    if "insta" in extracted_url:
      db_id = "your insta database-id"
    elif "reddit" in extracted_url:
      db_id = "your reddit database-id"
    elif "youtube" in extracted_url:
      db_id = "your youtube database-id"
    else:
      db_id = "your article database-id"
    return db_id
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------       
  token = pd.inputs["notion"]["$auth"]["oauth_access_token"]
  extracted_url = url()
  db_id = db_id_set((extracted_url))
  notion = Client(auth=token)
  title = name()
  tags = get_tags()
  
  new_page = {
    "URL": {
        "type": "url",
        "url": extracted_url
    },
    "Tags": {
        "type": "multi_select",
        "multi_select": tags
    },
    "Titel": {
        "type": "title",
        "title": [
            {
                "text": {
                    "content": title
                }
            }
        ]
    }
  }



  notion.pages.create(parent={"database_id": db_id}, properties=new_page)