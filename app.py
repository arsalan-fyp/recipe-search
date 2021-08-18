from flask import Flask,request,jsonify
import numpy as np
import pandas as pd

app = Flask(__name__)

df = pd.read_excel('./complete_recipes.xlsx')
df.dropna(inplace=True)

ingredientNames = set()

for ingredient in df['Ingredients']:
    singleIngredient = ingredient.split(";")
    
    for i in singleIngredient:
        ingredientNames.add(i.strip().split(":")[0].strip())

ingredientNames.remove('')
ingredient_list = list(ingredientNames) 

@app.route('/ingredient')
def getIngredientList():
    return {'ingredients':ingredient_list,'error':0}

@app.route('/all-recipes')
def getRecipes():
    return {'error':0, 'recipes':df.to_dict('r')}


@app.route('/recipe-by-ingredient',methods=['POST'])
def recipeByIngredients():
    selected_ingredients = request.json['ingredients']
    
    selected_recipes = []

    score = 0
    total_score = len(selected_ingredients)

    for index, recipe in df.iterrows():
        recipe_ingredient = recipe['Ingredients']
        
        for i in selected_ingredients:
            if(i.lower() in recipe_ingredient.lower()):
                score = score + 1
                
        achieve_score = int((score/total_score)*100)
        
        if(achieve_score > 35):
            selected_recipes.append(recipe)
            
        score = 0
    
    recipe_response = pd.DataFrame(selected_recipes).drop_duplicates().to_dict('r')
    
    return jsonify({'error':0,'recipes':recipe_response})


@app.route('/recipe-by-single-ingredient',methods=['POST'])
def recipeBySingleIngredients():
    selected_ingredients = request.json['ingredients']
    
    selected_recipes = []

    for index, recipe in df.iterrows():
        recipe_ingredient = recipe['Ingredients']
        
        for i in selected_ingredients:
            if(i.lower() in recipe_ingredient.lower()):
                selected_recipes.append(recipe)

    recipe_response = pd.DataFrame(selected_recipes).drop_duplicates().to_dict('r')
    
    return jsonify({'error':0,'recipes':recipe_response})
    

@app.route('/py_server')
def index():
    return 'Running Python Flask Server'

if __name__ == '__main__':
    app.run()