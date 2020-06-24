import pdfplumber
import json
import math
from decimal import Decimal

document_path = './data/0b3106da-a713-47b7-90c6-e665bdae74f3.pdf'
annotations_path = './data/0b3106da-a713-47b7-90c6-e665bdae74f3.json'

document = pdfplumber.open(document_path)
with open(annotations_path) as f:
  annotations = json.load(f)

def get_page(coordinate):
  return math.floor(coordinate)

def get_position(coordinate):
  return coordinate - get_page(coordinate)

def draw_page(page_number):
  page = document.pages[page_number - 1]
  page_annotations = filter(lambda annotation: any(map(lambda vertex: get_page(vertex["x"]) == page_number, annotation["vertices"])), annotations)
  image = page.to_image(resolution=100)

  print(f'page_number: {page_number}, width: {page.width}, height: {page.height}')

  for annotation in page_annotations:
    xs = list(map(lambda vertex: vertex["x"], annotation["vertices"]))
    ys = list(map(lambda vertex: vertex["y"], annotation["vertices"]))

    min_x = Decimal(get_position(min(xs))) * page.width
    max_x = Decimal(get_position(max(xs))) * page.width
    min_y = Decimal(get_position(min(ys))) * page.height
    max_y = Decimal(get_position(max(ys))) * page.height

    print(f'label: {annotation["label"]}, min_x: {min_x}, max_x: {max_x}, min_y: {min_y}, max_y: {max_y}')

    for vertex in annotation["vertices"]:
      image.draw_rect([min_x, max_y, max_x, min_y])

  image.save(f'out/page-{page_number}.png')

for page_number in range(1, len(document.pages) + 1):
  draw_page(page_number)
