from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import requests
import io
import time


def get_images_urls(driver, queries):
  images_urls = []
  names = []

  for q in queries:
    try:
      names.append(q[:-1])
      q = q.replace(' ', '+')
      query_url = f"https://www.google.com/search?q={q}&tbm=isch"
      driver.get(query_url)
      time.sleep(3)
      
      thumbnail = driver.find_element(By.CLASS_NAME, "Q4LuWd")
      thumbnail.click()
      time.sleep(3)

      image = driver.find_element(By.CLASS_NAME, "n3VNCb")
      if(image.get_attribute('src') and 'http' in image.get_attribute('src')):
        images_urls.append(image.get_attribute('src'))
      else:
        images_urls.append('None')
    except Exception as e:
      images_urls.append('None')
  return (images_urls, names)
  

def download_image(download_directory, url, file_name):
  try:
    image_content = requests.get(url).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file)

    file_path = download_directory + file_name

    with open(file_path, 'wb') as file:
      try:
        image.save(file, "JPEG")
      except:
        image.save(file, "PNG")
  except Exception as e:
    print(e)
  

def get_queries_from_file():
  queries = []
  try:
    file = open("Productos.txt", "r")
    for line in file:
      queries.append(line)
  except Exception as e:
    print(e)
  return queries


def main():
  queries = get_queries_from_file()

  driver = webdriver.Chrome()
  images_urls, names = get_images_urls(driver, queries)
  driver.close()
    
  output_file = open("enlaces.txt", "w")
  for element in images_urls:
    output_file.write(element + "\n")
    download_image("scraped_images/", element, names[images_urls.index(element)]+".jpg")
  output_file.close()

if __name__ == '__main__':
  main()