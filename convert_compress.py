import PIL
from PIL import Image
from fastapi import FastAPI
from pydantic import BaseModel

def image_compression(image_path, output_path):
    image_comp = image_path.convert("RGB")
    image_comp.save(output_path)

    statement = "Image converted and compressed successfully and saved at workdir"
    return statement

app = FastAPI()
class Item(BaseModel):
    image_path: str
    output_path: str

@app.get('/')
@app.post('/compress_and_convert_image/')
async def create_item(item:Item):
    item_dict = item.dict()
    a = item_dict['image_path']
    b = item_dict['output_path']
    img = Image.open(a)

    x = image_compression(img, b)
    return x

