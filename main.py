from flask import *
from werkzeug.utils import secure_filename
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute(
                "SELECT userId, firstName FROM users WHERE email = ?", (session['email'], ))
            userId, firstName = cur.fetchone()
            cur.execute(
                "SELECT count(mealId) FROM cart WHERE userId = ?", (userId, ))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)


@app.route("/")
def root():
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT mealid, name, price, description, image FROM meal_items')
        itemData = cur.fetchall()
        cur.execute('SELECT categoryId, name FROM categories')
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    return render_template('index.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, categoryData=categoryData, noOfItems=noOfItems)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('index.html', error=error)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))


def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False


@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Parse form data
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        state = request.form['state']
        phone = request.form['phone']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, state, phone) VALUES (?, ?, ?, ?, ?, ?)', (hashlib.md5(
                    password.encode()).hexdigest(), email, firstName, lastName, state, phone))

                con.commit()
                flash("Registered Successfully")
            except:
                con.rollback()
                flash("Error occured")
        con.close()
        return render_template("index.html")


@app.route("/manager")
def admin():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT categoryId, name FROM categories")
        categories = cur.fetchall()
    conn.close()
    return render_template('manager.html', categoryData=categories)


@app.route("/manageMeals")
def remove():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT mealId, name, price, description, image FROM meal_items')
        data = cur.fetchall()
    conn.close()
    return render_template('manage_meal.html', data=data)


@app.route("/removeItem")
def removeItem():
    mealId = request.args.get('mealId')
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM meal_items WHERE mealId = ?',
                        (mealId, ))
            conn.commit()
            msg = "Deleted successsfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    print(msg)
    return redirect(url_for('remove'))


@app.route('/addCategory', methods=["GET", "POST"])
def add_cat():
    if request.method == "POST":
        category = request.form['newCategory']
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    '''INSERT INTO categories (name) VALUES (?)''', (category,))
                conn.commit()
                msg = "inserted succesfully"
            except:
                msg = "error occured"
        conn.close()
        print(msg)
    return redirect(url_for('admin'))


@app.route("/displayCategory")
def displayCategory():
    loggedIn, firstName, noOfitems = getLoginDetails()
    categoryId = request.args.get("categoryId")
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT meal_items.mealId, meal_items.name, meal_items.price, meal_items.image, categories.name FROM meal_items, categories WHERE meal_items.categoryId = categories.categoryId AND categories.categoryId = ?", (categoryId, ))
        data = cur.fetchall()
    conn.close()
    categoryName = data[0][4]
    data = parse(data)
    return render_template('display_category.html', data=data, loggedIn=loggedIn, firstName=firstName, categoryName=categoryName, noOfitems=noOfitems)


@app.route("/mealDescription")
def mealDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    mealId = request.args.get('mealId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT mealId, name, price, description, image FROM meal_items WHERE mealId = ?', (mealId, ))
        Data = cur.fetchone()
    conn.close()
    return render_template("meal_description.html", data=Data, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)


@app.route('/manageCategory')
def show_cat():
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT categoryId, name FROM categories")
            categoryData = cur.fetchall()
            conn.commit()
            msg = "fetched succesfully"
        except:
            msg = "error occured"
        print(msg)
    return render_template('manage_categories.html', categoryData=categoryData)


@ app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        categoryId = int(request.form['category'])
        # Uploading image procedure
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
        with sqlite3.connect('database.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO meal_items (name, price, description, image, categoryId) VALUES (?, ?, ?, ?, ?)''',
                            (name, price, description, imagename, categoryId))
                conn.commit()
                msg = "added successfully"
            except:
                msg = "error occured"
                conn.rollback()
        conn.close()
        print(msg)
        return redirect(url_for('admin'))


@app.route("/removeCat", methods=["GET", "POST"])
def removeCat():
    with sqlite3.connect('database.db') as conn:
        try:
            category = request.form['category']
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM categories WHERE categoryId = ?", (category,))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
            print(msg)
    conn.close()
    return redirect(url_for('admin'))


@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        mealId = int(request.args.get('mealId'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = ?",
                        (session['email'], ))
            userId = cur.fetchone()[0]
            try:
                cur.execute(
                    "INSERT INTO cart (userId, mealId) VALUES (?, ?)", (userId, mealId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return redirect(url_for('root'))


@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT meal_items.mealId, meal_items.name, meal_items.price, meal_items.image FROM meal_items, cart WHERE meal_items.mealId = cart.mealId AND cart.userId = ?", (userId, ))
        meal_items = cur.fetchall()
    totalPrice = 0
    for row in meal_items:
        totalPrice += row[2]
    return render_template("cart.html", meal_items=meal_items, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)


@app.route("/checkout")
def checkout():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT meal_items.mealId, meal_items.name, meal_items.price, meal_items.image FROM meal_items, cart WHERE meal_items.mealId = cart.mealId AND cart.userId = ?", (userId, ))
        meal_items = cur.fetchall()
    totalPrice = 0
    for row in meal_items:
        totalPrice += row[2]
    return render_template("checkout.html", totalPrice=totalPrice)


@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    mealId = int(request.args.get('mealId'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        try:
            cur.execute(
                "DELETE FROM cart WHERE userId = ? AND mealId = ?", (userId, mealId))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('cart'))


def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


if __name__ == '__main__':
    app.run(debug=True)
