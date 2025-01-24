from fasthtml.common import *
from fasthtml.svg import *
from monsterui.franken import *
from monsterui.franken import Grid as Grd
from .blog_card import BlogCard
from modules.blog.models import BlogPost
from typing import List
def BlogList(posts: List[BlogPost]):
    """Blog posts list component."""
    return Section(
        Container(
            Grd(
                *[BlogCard(post) for post in posts],
                # cols=3,
                min_cols=1,
                max_cols=3,
                gap=6
            ),
            cls="mb-8"
        )
    ) 