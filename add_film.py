# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
# import django
# django.setup()
#
# import re
# import time
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from film.models import Movies
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Accept-Language': 'en-US,en;q=0.9'
# }
#
# def url_():
#     for count in range(1, 1000):
#         time.sleep(2)
#         url = f'https://www.metacritic.com/browse/movie/?releaseYearMin=1910&releaseYearMax=2024&page={count}'
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.text, 'lxml')
#         data = soup.find_all('div', class_="c-finderProductCard")
#
#         for movie in data:
#             movie_url = 'https://www.metacritic.com/' + movie.find('a').get('href')
#             yield movie_url
#
# chromedriver_path = 'C:\\Users\\averb\\PycharmProjects\\djangoProject\\chromedriver.exe'
# service = Service(chromedriver_path)
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(service=service, options=options)
#
# for movie_url in url_():
#     response = requests.get(movie_url, headers=headers)
#     soup = BeautifulSoup(response.text, 'lxml')
#
#     data = soup.find('div', class_="c-layoutDefault")
#     if not data:
#         continue
#
#     title_element = data.find('div', class_="c-productHero_title g-inner-spacing-bottom-medium g-outer-spacing-top-medium")
#     title = title_element.text if title_element else "Unknown Title"
#
#     valid_genres = ['Drama', 'Comedy', 'Adventure', 'Fantasy', 'Action', 'Thriller', 'Mystery', 'Romance', 'Sci-Fi', 'Horror', 'Documentary']
#     genre_pattern = re.compile('|'.join(valid_genres), re.IGNORECASE)
#
#     genres = soup.find_all('span', class_="c-globalButton_label")
#     genre = set([' '.join(genre.text.strip().split()) for genre in genres if genre_pattern.match(genre.text.strip())])
#
#     description_element = data.find('span', class_="c-productDetails_description g-text-xsmall")
#     description = description_element.text if description_element else "No description available"
#
#     release_date_element = data.find('li', class_="c-heroMetadata_item u-inline")
#     release_date = int(release_date_element.text.strip()) if release_date_element else None
#
#     rating_element = data.find('div', class_="c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green c-siteReviewScore_user g-color-gray90 c-siteReviewScore_medium")
#     rating = float(rating_element.text) if rating_element else 0.0
#
#     directors_element = data.find('p', class_="g-text-xxsmall")
#     directors = directors_element.text if directors_element else "Unknown Director"
#
#     review_count = 0
#
#     credits_url = movie_url + '/credits'
#     driver.get(credits_url)
#
#     wait = WebDriverWait(driver, 10)
#     try:
#         element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'picture.c-cmsImage.c-cmsImage-loaded img')))
#         image = element.get_attribute('src')
#     except:
#         image = None
#
#
#
#
#
#     movie_instance = Movies(
#         title=title,
#         genre=','.join(genre),
#         description=description,
#         release_date=release_date,
#         rating=rating,
#         review_count=review_count,
#         image=image,
#         directors=directors,
#     )
#     movie_instance.save()
#
# driver.quit()
