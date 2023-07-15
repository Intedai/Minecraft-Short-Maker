from bs4 import BeautifulSoup
from selenium import webdriver # Using Selenium because Cloudflare blocks get requests
from selenium.webdriver.firefox.service import Service
from os import path
from PIL import Image
from urllib.request import urlopen
from urllib.parse import urlparse, parse_qs

RENDERER_SIZE = 1080
SKIN_TYPES = ("slim", "classic")


def skin_img_renderer(id: str, type: str, theta: int, phi: int ) -> Image.Image:
    """
    Renders the Minecraft skin using the Namemc view skin link which generates an image.
    """

    return Image.open(urlopen(f"https://s.namemc.com/3d/skin/body.png?id={id}&model={SKIN_TYPES[type]}&theta={theta}&phi={phi}&time=0&width={RENDERER_SIZE}&height={RENDERER_SIZE}"))

def rt360render(id: str, type: str, phi: int, nid: int):
    """
    Uses skin_img_renderer to render in 360 degrees, in our case it renders in 0 and 180
    """
    for i in range(0, 360, 180):
        skin_img_renderer(id, type, i, phi).save(f"{nid} {i}.png")

def skin_info(skin_box) -> tuple:
    """
    Get information about the skin:
    ID, Render size, model type, Creator and link
    """
    # Get the id of the skin
    skinID = skin_box.a["href"][6:]

    # Creator of the skin
    skin_creator = skin_box.find('span').text

    # Link for the skin
    namemc_link = f"https://namemc.com/skin/{skinID}"

    # Get the image tag  which includes the src and in the src there is a query for model type
    img_tag = skin_box.find("img", class_="drop-shadow auto-size-square")
    
    # Get the data-src attribute
    data_src = img_tag.get("data-src")
    
    # Parse the URL
    url = urlparse(data_src)

    # Parse the query string
    query_dict = parse_qs(url.query)

    # Get the model from the model query, assign 0 for slim and 1 for classic
    model = 0 if query_dict.get('model')[0] == SKIN_TYPES[0] else 1

    return (skinID, RENDERER_SIZE, model, skin_creator, namemc_link)

def get_skins() -> list:
    """
    returns list of top 10 skins' info
    """
    # Skin list that will contain info
    skins = []
    
    # Don't log the webdriver
    service = Service(log_path=path.devnull)

    driver = webdriver.Firefox(service=service)

    # Get the weekly trending namemc pc
    driver.get('https://namemc.com/minecraft-skins/trending/weekly')
    
    # Get webpage html
    namemc_html = driver.page_source

    driver.close()

    soup = BeautifulSoup(namemc_html, 'html.parser')

    # Get skin boxes from page source
    skin_boxes = soup.findAll("div", class_="card mb-2")

    # Add the top 10 skins to the list
    for i, box in enumerate(skin_boxes, start=1):
        if i > 10:
            break
        skins.append(skin_info(box))
    
    return skins