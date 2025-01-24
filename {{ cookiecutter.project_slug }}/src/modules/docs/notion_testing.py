from notion_client import Client
import os
from typing import List, Dict, Any
notion = Client(auth=os.environ["NOTION_KEY"])

# %%
def get_all_databases(notion_client: Client) -> List[Dict[Any, Any]]:
    """
    Retrieve all databases accessible to the Notion integration.
    
    Args:
        notion_client: An authenticated Notion client instance
        
    Returns:
        List of dictionaries containing database information
    """
    databases = []
    start_cursor = None
    
    while True:
        # Make the API request with pagination
        response = notion_client.search(
            filter={
                "property": "object",
                "value": "database"
            },
            start_cursor=start_cursor,
            page_size=100  # Maximum allowed by Notion API
        )
        
        # Add the databases from current page to our results
        databases.extend(response["results"])
        
        # Check if there are more results
        if not response["has_more"]:
            break
            
        # Update the cursor for the next page
        start_cursor = response["next_cursor"]
    
    return databases

# response = notion.search(
#     filter={"property": "object", "value": "database"},
#     start_cursor=None,
#     page_size=100,  # Maximum allowed by Notion API
# )
# for db in response["results"]:
#     print(f"Database: {db['title'][0]['plain_text']} (ID: {db['id']})")
# %%
