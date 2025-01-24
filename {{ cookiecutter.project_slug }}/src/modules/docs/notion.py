from fasthtml.common import *
from monsterui import *
from monsterui.franken import *
from notion_client import Client
from config import Settings
from typing import List, Dict, Any
notion_key = Settings().notion_key
notion = Client(auth=notion_key)
class NotionPage:
    def __init__(self):
        self.notion = Client(auth=notion_key)

    def get_page_blocks(self, page_id: str) -> list:
        """Fetch all blocks for a page"""
        if "notion.so" in page_id:
            page_id = page_id.split("/")[-1].split("-")[-1]

        return self._fetch_blocks_with_children(page_id)

    def _fetch_blocks_with_children(self, block_id: str) -> list:
        """Recursively fetch blocks and their children"""
        blocks = []
        cursor = None

        while True:
            response: dict = self.notion.blocks.children.list(
                block_id=block_id, start_cursor=cursor
            )

            # Process each block and fetch its children if it has them
            for block in response["results"]:
                # Check if block has children
                if block.get("has_children"):
                    block["children"] = self._fetch_blocks_with_children(block["id"])
                blocks.append(block)

            if not response.get("has_more"):
                break

            cursor = response["next_cursor"]

        return blocks

    def blocks_to_components(self, blocks: list) -> list:
        """Convert Notion blocks to FastHTML components"""
        components = []
        rendered = []
        for block in blocks:
            # try:
            block_type = block["type"]
            component = None
            if (
                block["parent"]["type"] == "block_id"
                and block["parent"]["block_id"] in rendered
            ):
                continue
            # Handle the block based on its type
            if block_type == "paragraph":
                text = self._get_text(block["paragraph"])
                if text:
                    component = P(text)
                    if block.get("children"):
                        # Add child components indented
                        child_components = self.blocks_to_components(block["children"])
                        component = Div(
                            component,
                            Div(*child_components, cls="pl-6"),
                            cls="paragraph-with-children",
                        )
                else:
                    component = P("Empty paragraph")

            elif block_type == "heading_1":
                if block.get("has_children"):
                    component = self._handle_toggle_heading(block, "h1")
                else:
                    component = H1(self._get_text(block["heading_1"]))

            elif block_type == "heading_2":
                if block.get("has_children"):
                    component = self._handle_toggle_heading(block, "h2")
                else:
                    component = H2(self._get_text(block["heading_2"]))

            elif block_type == "heading_3":
                if block.get("has_children"):
                    component = self._handle_toggle_heading(block, "h3")
                else:
                    component = H3(self._get_text(block["heading_3"]))

            elif block_type == "bulleted_list_item":
                text = self._get_text(block["bulleted_list_item"])
                component = Li(text)
                if block.get("children"):
                    child_components = self.blocks_to_components(block["children"])
                    # For list items, nest the children in a new UL
                    component = Li(text, Ul(*child_components, cls="pl-6"))

            elif block_type == "numbered_list_item":
                text = self._get_text(block["numbered_list_item"])
                component = Li(text)
                if block.get("children"):
                    child_components = self.blocks_to_components(block["children"])
                    # For list items, nest the children in an OL
                    component = Li(text, Ol(*child_components, cls="pl-6"))

            elif block_type == "toggle":
                text = self._get_text(block["toggle"])
                if block.get("children"):
                    child_components = self.blocks_to_components(block["children"])
                    # Create a toggle-like component using a details element
                    component = Details(
                        Summary(text),
                        Div(*child_components, cls="pl-6"),
                        cls="toggle",
                    )
                else:
                    component = Details(Summary(text), cls="toggle")

            elif block_type == "divider":
                component = Hr()

            elif block_type == "image":
                component = self._handle_image_block(block)
            elif block_type == "to_do":
                component = self._handle_todo_block(block)
            elif block_type == "quote":
                component = self._handle_quote_block(block)
            elif block_type == "callout":
                component = self._handle_callout_block(block)
            elif block_type == "video":
                component = self._handle_video_block(block)
            elif block_type == "code":
                component = self._handle_code_block(block)

            if component is not None:
                components.append(component)
                rendered.append(block["id"])
            else:
                print(f"Unsupported block type: {block_type}")

        # except Exception as e:
        #     print(f"Error processing block {block}: {str(e)}")
        #     continue

        return components or [P("No content found")]

    def _handle_toggle_block(self, block: dict) -> FT:
        """Handle a basic toggle block"""
        text = self._get_text(block["toggle"])
        content = []

        # Add any children blocks
        if block.get("children"):
            child_components = self.blocks_to_components(block["children"])
            content.extend(child_components)

        return Details(
            Summary(
                text, cls="cursor-pointer hover:bg-gray-100 p-2 rounded"
            ),
            Div(*content, cls="pl-6 py-2"),
            cls="mb-4",
        )

    def _handle_toggle_heading(self, block: dict, level: str) -> FT:
        """Handle a toggle heading block"""
        # Get heading text and create appropriate heading element
        heading_type = f"heading_{level[-1]}"  # converts 'h1' to 'heading_1'
        text = self._get_text(block[heading_type])

        if level == "h1":
            heading = H1(text)
        elif level == "h2":
            heading = H2(text)
        else:
            heading = H3(text)

        content = []

        # Add any children blocks
        if block.get("children"):
            child_components = self.blocks_to_components(block["children"])
            content.extend(child_components)

        return Details(
            Summary(
                text,
                cls=f"uk-{level} toggle cursor-pointer p-2 rounded",
            ),
            Div(*content, cls="pl-6 py-2"),
            cls=f"toggle-heading-{level} mb-4",
            # style=toggle_styles,
        )

    def _handle_toggle_list(self, block: dict) -> FT:
        """Handle a toggle that contains a list"""
        text = self._get_text(block["toggle"])
        content = []

        # Check if children are list items
        if block.get("children"):
            list_items = []
            child_components = []

            for child in block["children"]:
                if child["type"] in ["bulleted_list_item", "numbered_list_item"]:
                    list_items.append(Li(self._get_text(child[child["type"]])))
                else:
                    child_components.extend(self.blocks_to_components([child]))

            # If we have list items, wrap them in appropriate list element
            if list_items:
                # Use numbered list if first child is numbered
                if block["children"][0]["type"] == "numbered_list_item":
                    content.append(Ol(*list_items, cls="list-decimal pl-6"))
                else:
                    content.append(Ul(*list_items, cls="list-disc pl-6"))

            # Add any non-list components
            content.extend(child_components)

        return Details(
            Summary(
                text,
                cls="toggle-list-summary cursor-pointer hover:bg-gray-100 p-2 rounded",
            ),
            Div(*content, cls="pl-6 py-2"),
            cls="toggle-list mb-4",
        )

    def _handle_image_block(self, block: dict) -> FT:
        """Handle different types of image blocks"""
        image = block["image"]
        caption = self._get_text(image) if image.get("caption") else None

        # Handle external images
        if image["type"] == "external":
            url = image["external"]["url"]
        # Handle uploaded images
        elif image["type"] == "file":
            url = image["file"]["url"]
        else:
            return P("Unsupported image type")

        # Create figure with optional caption
        img = Img(
            src=url,
            alt=caption or "Notion image",
            cls="notion-image w-full max-w-3xl mx-auto rounded-lg shadow-lg",
            loading="lazy",
        )

        if caption:
            return Figure(
                img,
                Figcaption(caption, cls="text-center text-sm text-gray-600 mt-2"),
                cls="my-4",
            )

        return Div(img, cls="my-4")

    def _handle_todo_block(self, block: dict) -> FT:
        """Handle a to-do block"""
        todo = block["to_do"]
        text = self._get_text(todo)
        checked = todo.get("checked", False)
        label = LabelCheckboxX(text, checked=checked, disabled=True, cls="mb-1")

        if block.get("children"):
            child_components = self.blocks_to_components(block["children"])
            return Div(label, Div(*child_components, cls="pl-6 mt-2"), cls="mb-1")
        # return Div(P(label + " " + text, cls="mb-0"), cls="mb-4")
        return label

    def _handle_quote_block(self, block: dict) -> FT:
        """Handle a quote block"""
        text = self._get_text(block["quote"])

        component = Blockquote(P(text), cls="border-l-4 border-gray-300 pl-4 my-4")

        if block.get("children"):
            child_components = self.blocks_to_components(block["children"])
            return Div(component, Div(*child_components, cls="pl-6"), cls="quote-block")

        return component

    def _handle_callout_block(self, block: dict) -> FT:
        """Handle a callout block"""
        callout = block["callout"]
        text = self._get_text(callout)
        icon = callout.get("icon", {})

        # Handle emoji icon
        icon_element = None
        if icon.get("type") == "emoji":
            icon_element = Span(icon["emoji"], cls="mr-2")

        callout_content = [P(text, cls="mb-0")]

        if block.get("children"):
            child_components = self.blocks_to_components(block["children"])
            callout_content.append(Div(*child_components, cls="mt-2"))

        return Div(
            Div(
                icon_element if icon_element else None,
                *callout_content,
                cls="flex p-4 bg-accent rounded-lg",  # TODO parametrize color?
            ),
            cls="callout-block my-4",
        )

    def _handle_video_block(self, block: dict) -> FT:
        """Handle a video block"""
        video = block["video"]
        video_type = video["type"]  # 'external' or 'file'
        caption = self._get_text(video) if video.get("caption") else None

        if video_type == "external":
            url = video["external"]["url"]

            # Handle YouTube URLs
            if "youtube.com" in url or "youtu.be" in url:
                # Convert to embed URL if needed
                if "watch?v=" in url:
                    video_id = url.split("watch?v=")[1].split("&")[0]
                    embed_url = f"https://www.youtube.com/embed/{video_id}"
                elif "youtu.be" in url:
                    video_id = url.split("youtu.be/")[1]
                    embed_url = f"https://www.youtube.com/embed/{video_id}"
                else:
                    embed_url = url

                video_component = ft(
                    "iframe",
                    src=embed_url,
                    cls="w-full aspect-video rounded-lg",
                    loading="lazy",
                    frameborder="0",
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
                    allowfullscreen=True,
                )
            else:
                # For other video providers, just link to the video
                video_component = A(
                    "Watch video",
                    href=url,
                    target="_blank",
                    cls="text-blue-500 hover:underline",
                )

        if caption:
            return Figure(
                video_component,
                Figcaption(caption, cls="text-center text-sm text-gray-600 mt-2"),
                cls="video-block my-4",
            )

        return Div(video_component, cls="video-block my-4")

    def _handle_code_block(self, block: dict) -> FT:
        """Handle a code block"""
        code = block["code"]
        text = self._get_text(code)
        language = code.get("language", "plain text")
        caption = self._get_text(code) if code.get("caption") else None


        code_block = Pre(
            Code(text),
            cls=f"relative rounded-lg overflow-x-auto language-{language}",
        )

        if caption:
            return Div(
                code_block,
                P(caption, cls="text-sm text-gray-600 mt-2"),
                cls="code-block my-4",
            )

        return Div(code_block, cls="code-block my-4")

    def _get_text(self, block_content: dict) -> str:
        """Extract text content from a block"""
        if not block_content.get("rich_text"):
            return " "
        return " ".join(text["plain_text"] for text in block_content["rich_text"])


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

def dbs_with_links():
    databases = get_all_databases(notion)
    dbs_with_links = [] 
    for db in databases:
        if db["url"]:
            dbs_with_links.append(Li(A(db["title"][0]["plain_text"], href=db["url"])))
    return dbs_with_links
