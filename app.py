from flask import Flask
from flask import render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
db = SQLAlchemy(app)
app.app_context().push()


class Categories(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    tasks = db.relationship("Tasks", backref="category", lazy=True, order_by="Tasks.date")


class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete = "CASCADE"), nullable=False)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return "Hi"
    else:
        cats = Categories.query.all()
        tasks_by_category = {category: category.tasks for category in cats}
        return render_template("to_do_list.html", tasks_by_category=tasks_by_category)


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        cat = request.form["cat_name"]
        task = request.form["task_name"]
        date = request.form["date_name"]

        if date:
            year = date[0:4] 
            month = date[5:7]
            if month[0] == "0":
                month = month[1]
            day = date[8:10] 
            if day[0] == "0":
                day = day[1]    
            date = f"{month}/{day}/{year}"     

        new_task = Tasks(name=task, date=date, category_id=cat)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your task"
    else:
        cats = Categories.query.all()
        return render_template("add_task.html", cats=cats)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        cat = request.form["cat_name"]
        new_cat = Categories(name=cat)
        try:
            db.session.add(new_cat)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your category"
    else:
        return render_template("add_cat.html")
    
@app.route("/delete_task/<int:id>", methods=["POST"])
def delete_task(id):
    task_to_delete = Tasks.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"

@app.route("/delete_category/<int:id>", methods=["POST"])
def delete_category(id):
    category_to_delete = Categories.query.get_or_404(id)
    try:
        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that category"
    
@app.route("/edit_category/<int:id>", methods=["GET", "POST"])
def edit_category(id):
    category_to_edit = Categories.query.get_or_404(id)
    if request.method == "POST":
        category_to_edit.name = request.form["new_cat"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem editing that category"

    else:
        return render_template("edit_cat.html", category_to_edit = category_to_edit)

@app.route("/edit_task/<int:id>", methods = ["GET", "POST"])
def edit_task(id):
    task_to_edit = Tasks.query.get_or_404(id)
    if request.method == "POST":
        new_name = request.form["new_task"]
        new_date = request.form["new_date"]
        if new_name != "":
            task_to_edit.name = new_name
        if new_date != "":
            year = new_date[0:4] 
            month = new_date[5:7]
            if month[0] == "0":
                month = month[1]
            day = new_date[8:10] 
            if day[0] == "0":
                day = day[1]    
            new_date = f"{month}/{day}/{year}"
            task_to_edit.date = new_date 
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem editing that task"
    else:
        return render_template("edit_task.html", task_to_edit = task_to_edit)
    
@app.route("/calendar")
def calendar():
    tasks = Tasks.query.all()
    Monday = []
    Tuesday = []
    Wednesday = []
    Thursday = []
    Friday = []
    Saturday = []
    Sunday = []
    for task in tasks:
        date_str = task.date
        date_obj = datetime.strptime(date_str, "%m/%d/%Y")
        date_day = date_obj.weekday()
        if date_day == 0:
            Monday.append(task)
        elif date_day == 1:
            Tuesday.append(task)
        elif date_day == 2:
            Wednesday.append(task)
        elif date_day == 3:
            Thursday.append(task)
        elif date_day == 4:
            Friday.append(task)
        elif date_day == 5:
            Saturday.append(task)
        elif date_day == 6:
            Sunday.append(task)
    return render_template("calendar.html", Monday=Monday, Tuesday=Tuesday, Wednesday=Wednesday, Thursday=Thursday, Friday=Friday, Saturday=Saturday, Sunday=Sunday)

@app.route("/journal", methods = ["GET"])
def journal():
    note = Notes.query.first()
    content = note.content if note else ""
    return render_template("journal.html", content = content)

@app.route("/save_notes", methods = ["POST"])
def save_notes():
    data = request.get_json()
    content = data.get("notes", "")
    note = Notes.query.first()
    if note:
        note.content = content
    try:
        db.session.commit()
        return jsonify({"status": "success", "message": "Notes saved successfully"})
    except:
        return jsonify({"status": "error", "message": "Did not save"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)

