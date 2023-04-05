class DishCrawler:
    def __init__(self, soup):
        self.soup = soup

    def extractDishName(self):
        return self.soup.find('div', 'view2_summary').find('h3').get_text()

    def extractDishImageUrl(self):
        return self.soup.find('div', 'centeredcrop').find('img').get('src')

    def extractDishExplain(self):
        return self.soup.find('div', 'view2_summary_in').get_text().replace('\n', '').strip()

    def extractDishIngredients(self):
        ingredients = []
        for liTag in self.soup.find('div', 'ready_ingre3').find_all('li'):
            name = liTag.next.strip()
            amount = liTag.find('span').get_text()

            ingredients.append({
                "name": name,
                "amount": amount,
            })
        return ingredients

    def extractDishRecipeSteps(self):
        recipeSteps = []

        count = 1
        for recipeStep in self.soup.find_all('div', 'view_step')[1].find_all('div', 'view_step_cont'):
            recipeText = recipeStep.get_text().replace('\n', ' ')
            recipeImgUrl = recipeStep.find('img').get('src')

            recipeSteps.append({
                "stepNumber": count,
                "text": recipeText,
                "imageUrl": recipeImgUrl
            })
            count += 1
        return recipeSteps

    def extractDishTip(self):
        return self.soup.find('dl', 'view_step_tip').find('dd').get_text()