# app/pages/index.py
from fasthtml.common import *
from fasthtml.core import APIRouter
from monsterui import *
from monsterui.all import *
from modules.public.components.hero import HeroSection
from modules.public.components.ctas import ctas
from modules.public.components.footer import footer
from modules.public.components.features import FeaturesSection
from modules.shared.templates import page_template
from config import Settings
config = Settings()
rt = APIRouter()



@rt("/")
@page_template(title=config.app_name + " - Build Faster")
def get(request):
    return Div(HeroSection(), ctas(),FeaturesSection(), footer())