from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Configuração Inicial:
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
#Configura o banco de dados SQLite chamado blog.db.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#Inicializa o SQLAlchemy com o aplicativo Flask.


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    posts = Post.query.all()
    return  render_template('home.html', posts=posts)

@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/criar', methods=['GET', 'POST'])
def criar_post():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        conteudo = request.form.get('conteudo')
        novo_post = Post(titulo=titulo, conteudo=conteudo)
        db.session.add(novo_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('criar_post.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.titulo = request.form.get('titulo')
        post.conteudo = request.form.get('conteudo')
        db.session.commit()
        return redirect(url_for('post', id=post.id))
    return render_template('editar_post.html', post=post)

@app.route('/deletar/<int:id>')
def deletar_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




