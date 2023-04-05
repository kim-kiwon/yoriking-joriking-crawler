import requests
from bs4 import BeautifulSoup

class RecipeUrlCrawler:
    def __init__(self):
        pass

    def extractRecipeUrlsByRecommnadUrl(self, recommendUrl):
        recipeBaseUrl = "http://www.10000recipe.com"

        response = requests.get(recommendUrl)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        aTags = soup.find_all('a', 'common_sp_link')
        dishUrls = list(map(lambda link: recipeBaseUrl + link.get('href'), aTags))
        print(dishUrls)
        return dishUrls