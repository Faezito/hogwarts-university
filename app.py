from flask import Flask, render_template, request, url_for, redirect, flash, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = '1234'

def get_user(username):
    conn = sqlite3.connect('unihog.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()
    return user


@app.route('/')
def index():
    return render_template('index.html', page_css = 'login.css')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash('Preencha todos os campos!', 'error')
            return render_template('index.html', page_css='login.css')

        user = get_user(username)

        if user:
            hashed_password = user[6]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                session['username'] = username
                session['cargo'] = user[8]
                return redirect(url_for('profile', username=username))
            else:
                flash('Usuario ou senha inválidos!', 'error')

        return redirect(url_for('index'))

@app.route('/user/<username>')
def profile(username):

    if 'username' not in session or session['username'] != username:    
        flash('Você não está logado', 'error')
        return redirect(url_for('index'))

    conn = sqlite3.connect('unihog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT firstName, lastName, cargo FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        first_name = user[0]
        last_name = user[1]
        cargo = user[2]
        nome_completo = f"{first_name} {last_name}"
        return render_template('main.html', page_css='main.css', nome=nome_completo, cargo=cargo)
    else:
        flash("Usuário não encontrado!", "error")
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Você se desconectou.", "success")
    return redirect(url_for('index'))

@app.route('/addUser', methods=['POST'])
def addUser(): 

    username = request.form.get('username')
    firstName = request.form.get('firstName')
    middleName = request.form.get('middleName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')
    password = request.form.get('password')
    classe_id = request.form.get('classeID')
    cargo = request.form.get('cargo')

    if not all([firstName, lastName, username, email, password, cargo]):
        flash("Erro: Preencha todos os campos!", "error")
        return redirect(url_for('profile', username=session.get("username")))
    
    conn = sqlite3.connect('unihog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
    user = cursor.fetchone()

    if user:
        conn.close()
        flash("Erro: Usuário ou e-mail já cadastrado")
        return redirect(url_for('profile', username=session.get("username")))

    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute('INSERT INTO users (firstName, lastName, middleName, username, email, password, classe_id, cargo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                   (firstName, middleName, lastName, username, email, hashedPassword.decode('utf-8'), classe_id, cargo))
    conn.commit()
    conn.close()

    flash("Usuário adicionado com sucesso", "success")
    return redirect(url_for("profile", username=session.get("username")))


@app.route('/content/addUser')
def content_addUser():
    return render_template("content/addUser.html")


@app.route('/funcList')
def funcList():
    conn = sqlite3.connect('unihog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT firstName, lastName, cargo FROM users')
    users = cursor.fetchall()
    conn.close()

    listaFuncionarios = []

    for user in users:
        firstName, lastName, cargo = user
        nomeCompleto = f'{firstName} {lastName}'
        listaFuncionarios.append({'nome': nomeCompleto, 'cargo': cargo})

    return render_template("content/lista-de-funcionarios.html", funcionarios=listaFuncionarios)


if __name__ == "__main__":
    app.run(debug=True)