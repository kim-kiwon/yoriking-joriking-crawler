import mysql.connector
from datetime import datetime

class DishRepository:
    def __init__(self, config):
        self.cnx = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"]
        )
        self.cursor = self.cnx.cursor()

    def insertDish(self, dishName, dishImageUrl, dishExplain, dishTip):
        # dishName이 이미 DB에 삽입되었는지 확인
        selectDishSql = "SELECT id FROM dish WHERE dish_name = %s"
        self.cursor.execute(selectDishSql, (dishName,))
        result = self.cursor.fetchone()

        # 삽입되지 않았다면 삽입하고 dishId 반환
        if result is None:
            now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            insertDishSql = 'INSERT INTO dish (dish_name, dish_image_url, dish_explain, dish_tip, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)'
            params = (dishName, dishImageUrl, dishExplain, dishTip, now, now)
            self.cursor.execute(insertDishSql, params)
            self.cnx.commit()

            return self.cursor.lastrowid

        # 삽입되었다면 해당 요리는 건너뛰게 분기치려고 None 반환
        return None

    def insertIngrdientAndDishIngredient(self, dishId, ingredients):
        for ingredient in ingredients:
            ingredientName = ingredient["name"]
            ingredientAmount = ingredient["amount"]

            # Ingredeint 와 DishIngredient 삽입
            ingredientId = self._insertIngredient(ingredientName)
            self._insertDishIngredient(dishId, ingredientId, ingredientAmount)


    def insertRecipeAndRecipeStep(self, dishId, recipe):
        recipeId = self._insertRecipe(dishId)
        self._insertRecipeStep(recipeId, recipe)

    def _insertIngredient(self, ingredientName):
        # ingredientName이 이미 DB에 삽입되었는지 확인
        selectIngredientSql = "SELECT id FROM ingredient WHERE ingredient_name = %s"
        self.cursor.execute(selectIngredientSql, (ingredientName,))
        result = self.cursor.fetchone()

        # 삽입되지 않았다면 삽입하고 ingredientId 반환
        if result is None:
            now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            insertIngredientSql = 'INSERT INTO ingredient (ingredient_name, created_at, updated_at) VALUES (%s, %s, %s)'
            self.cursor.execute(insertIngredientSql, (ingredientName, now, now))
            self.cnx.commit()
            return self.cursor.lastrowid

        # 삽입되어 있다면 해당 ingredientId 반환
        return result[0]

    def _insertDishIngredient(self, dishId, ingredientId, ingredientAmount):
        # dishIngredient가 이미 DB에 삽입되었는지 확인
        selectDishIngredientSql = "SELECT id FROM dish_ingredient WHERE dish_id = %s AND ingredient_id = %s"
        self.cursor.execute(selectDishIngredientSql, (dishId, ingredientId))
        result = self.cursor.fetchone()

        # 삽입되지 않았다면 삽입하고 해당 dishIngredientId 반환
        if result is None:
            now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            insertDishIngredientSql = 'INSERT INTO dish_ingredient (dish_id, ingredient_id, ingredient_amount, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)'
            self.cursor.execute(insertDishIngredientSql, (dishId, ingredientId, ingredientAmount, now, now))
            self.cnx.commit()

            return self.cursor.lastrowid

        # 삽입되어 있다면 해당 dishIngredientId 반환
        return result[0]

    def _insertRecipe(self, dishId):
        # recipe 가 이미 DB에 삽입되었는지 확인
        selectRecipeSql = "SELECT id FROM recipe WHERE dish_id = %s"
        self.cursor.execute(selectRecipeSql, (dishId,))
        result = self.cursor.fetchone()

        # 삽입되지 않았다면 삽입하고 해당 recipeId 반환
        if result is None:
            now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            insertRecipeSql = 'INSERT INTO recipe (dish_id, created_at, updated_at) VALUES (%s, %s, %s)'
            self.cursor.execute(insertRecipeSql, (dishId, now, now))
            self.cnx.commit()
            return self.cursor.lastrowid

        # 삽입되어 있다면 해당 recipeId 반환
        return result[0]

    def _insertRecipeStep(self, recipeId, recipe):
        for recipeStep in recipe:
            # 해당 recipeStep 이 이미 DB에 삽입되었는지 확인
            selectRecipeStepSql = "SELECT id FROM recipe_step WHERE recipe_id = %s and step_number = %s"
            self.cursor.execute(selectRecipeStepSql, (recipeId, recipeStep["stepNumber"]))
            result = self.cursor.fetchone()

            # 삽입되지 않았다면 삽입
            if result is None:
                now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                insertRecipeSql = 'INSERT INTO recipe_step (step_number, recipe_text, recipe_image_url, recipe_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)'
                self.cursor.execute(insertRecipeSql,
                                    (recipeStep["stepNumber"], recipeStep["text"], recipeStep["imageUrl"], recipeId, now,
                                     now))
                self.cnx.commit()

    def __del__(self):
        self.cursor.close()
        self.cnx.close()