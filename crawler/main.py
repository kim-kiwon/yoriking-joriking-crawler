import configparser
import requests
from bs4 import BeautifulSoup
import time
import random

from recipe_url_crawler import RecipeUrlCrawler
from dish_crawler import DishCrawler
from dish_repository import DishRepository

RECOMMAND_START_INDEX = 1
RECOMMNAD_END_INDEX = 500

def crawling(start, end):
    mysqlConfig = getMysqlConfig()

    for recommendIndex in range(start, end+1):
        recommendUrl = "https://www.10000recipe.com/recipe/list.html?order=reco&page=" + str(recommendIndex)

        sleepRandom()
        recipeUrlCrawler = RecipeUrlCrawler()
        recipeUrls = recipeUrlCrawler.extractRecipeUrlsByRecommnadUrl(recommendUrl)

        for recipeUrl in recipeUrls:
            sleepRandom()
            response = requests.get(recipeUrl)
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')

            dishCrawler = DishCrawler(soup)

            try:
                dishName = dishCrawler.extractDishName()
                ingredients = dishCrawler.extractDishIngredients()
                recipeSteps = dishCrawler.extractDishRecipeSteps()
            except(AttributeError):
                continue

            try:
                dishImageUrl = dishCrawler.extractDishImageUrl()
            except(AttributeError):
                dishImageUrl = None
                pass

            try:
                dishExplain = dishCrawler.extractDishExplain()
            except(AttributeError):
                dishExplain = None
                pass

            try:
                dishTip = dishCrawler.extractDishTip()
            except(AttributeError):
                dishTip = None
                pass

            dishRepository = DishRepository(mysqlConfig)

            dishId = dishRepository.insertDish(dishName, dishImageUrl, dishExplain, dishTip)
            if dishId is None:
                continue

            dishRepository.insertIngrdientAndDishIngredient(dishId, ingredients)
            dishRepository.insertRecipeAndRecipeStep(dishId, recipeSteps)

def getMysqlConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')

    return {
        'host': config.get('mysql', 'host'),
        'user': config.get('mysql', 'user'),
        'password': config.get('mysql', 'password'),
        'database': config.get('mysql', 'database')
    }

def sleepRandom():
    time.sleep(random.uniform(2, 4))

if __name__ == '__main__':
    crawling(RECOMMAND_START_INDEX, RECOMMNAD_END_INDEX)