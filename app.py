from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kulblog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    ingr = db.Column(db.String(500), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return 'Recipes %r' %self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts/<string:id>/delete')
def post_delete(id):
    recipe = Recipes.query.get_or_404(id)
    try:
        db.session.delete(recipe)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении рецепта произошла ошибка"

@app.route('/posts/<string:id>')
def post_detail(id):
    recipe = Recipes.query.get(id)
    return render_template('post_detail.html', recipe = recipe)

@app.route('/posts')
def posts():
    recipes = Recipes.query.order_by(Recipes.date.desc()).all()
    return render_template('posts.html', recipes = recipes)

@app.route('/posts/<string:id>/update', methods = ['POST', 'GET'])
def post_update(id):
    recipe = Recipes.query.get(id)
    if request.method == "POST":
        recipe.title = request.form['title']
        recipe.ingr = request.form['ingr']
        recipe.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При загрузке рецепта произошла ошибка"
    else:
        recipe = Recipes.query.get(id)
        return render_template('post_update.html', recipe = recipe)

@app.route('/create-recipes', methods = ['POST', 'GET'])
def create_recipes():
    if request.method == "POST":
        title = request.form['title']
        ingr = request.form['ingr']
        text = request.form['text']

        recipe = Recipes(title = title, ingr = ingr, text = text)

        try:
            db.session.add(recipe)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При загрузке рецепта произошла ошибка"
    else:
        return render_template('create_recipes.html')

if __name__ == '__main__':
    app.run(debug=True)