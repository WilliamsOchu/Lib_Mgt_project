## Import necessary dependencies
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from config import Config
import MySQLdb.cursors
import os
import mysql.connector
from mysql.connector import Error

## Initiate Flask app and MYSQL Database
app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

## Flask app landing page
@app.route('/')
def index():
    return render_template('index.html')

## Register New User
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (first_name, last_name, email, password, role) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, email, password, role))
        mysql.connection.commit()
        cur.close()
        flash('User Added Successfully!')
        return render_template('register.html')

## User Login Page
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s AND role = % s', (email, password, role ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['email'] = user['email']
            session['role'] = user['role']
            mesage = 'Logged in successfully!'
            return redirect(url_for('welcome'))               
    return render_template('login.html', mesage = mesage)

## View Users
@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('users_list.html', users=users)


## Add and View Books
@app.route('/books')
def books():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    return render_template('books.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        genre = request.form['genre']
        publication_date = request.form['publication_date']
        publisher = request.form['publisher']
        no_of_copy = request.form['no_of_copy']
        categoryid = request.form['categoryid']
        rackid = request.form['rackid']
        added_on = request.form['added_on']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books (title, author, isbn, genre, publication_date, publisher, no_of_copy, categoryid, rackid, added_on) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (title, author, isbn, genre, publication_date, publisher, no_of_copy, categoryid, rackid, added_on))
        mysql.connection.commit()
        cur.close()
        flash('Book Added Successfully!')
        return redirect(url_for('books'))

## Add User
@app.route('/add_user', methods=['GET' 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (first_name, last_name, email, password, role) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, email, password, role))
        mysql.connection.commit()
        cur.close()
        flash('User Added Successfully!')
        return redirect(url_for('users'))
    
    
## Succesful Auth Landing Page        
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

## Admin Landing Page
@app.route('/admins')
def admins():
    return render_template('admins.html')

## Librarian Landing Page
@app.route('/lib_welcome')
def lib_welcome():
    return render_template('lib_welcome.html')

## Member Landing Page
@app.route('/mem_welcome')
def mem_welcome():
    return render_template('mem_welcome.html')

## Borrow Book
@app.route('/borrow')
def borrow():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    return render_template('book_list.html', books=books)

## View Books 
@app.route('/book_list', methods=['POST'])
def book_list():    
    if request.method == 'POST':
        title = request.form['title']
        no_of_copy = request.form['no_of_copy']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO borrowed (title, no_of_copy) VALUES (%s, %s)", (title, no_of_copy))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('borrowed'))   
    return render_template('book_list.html', books=books)

## View Borrowed History
@app.route('/borrowed')
def borrowed():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM borrowed")
    borrowed = cur.fetchall()
    cur.close()
    return render_template('borrowed.html', borrowed=borrowed)

## List Users
@app.route("/adminlist", methods =['GET'])
def admins_list_user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('loggedin.html', users=users)

## Delete Users
@app.route('/kill_user')
def kill_user():
    email = request.form.get('email')
    if 'loggedin' in session:
        #deleteUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM users WHERE email = % s', (email, ))
        mysql.connection.commit()   
        return render_template('loggedin.html')
    return redirect(url_for('login'))

## Book Reviews
@app.route('/av_reviews', methods=['POST'])
def av_reviews():
    if request.method == 'POST':
        title = request.form['title']
        rating = request.form['rating']
        review = request.form['review']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO reviews (title, rating, review) VALUES (%s, %s, %s)", (title, rating, review))
        mysql.connection.commit()
        cur.close()
        flash('Review Added Successfully!')
        return render_template('borrowed.html')
    
## Show Book Reviews  
@app.route("/reviews", methods =['GET'])
def reviews():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reviews")
    reviews = cur.fetchall()
    cur.close()
    return render_template('reviews.html', reviews=reviews)

## User Logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect(url_for('index'))

## Terminate flask app
@app.route('/shutdown')
def shutdown():
    os._exit(0)


if __name__ == '__main__':
    app.run(debug=True)
