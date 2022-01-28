from PIL import Image

def thumbnail(image: str, thumbnail: str) -> None:
    resize = (128, 128)
    img = Image.open(image)
    img = img.resize(resize, Image.ANTIALIAS)
    img.save(thumbnail)
