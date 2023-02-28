from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mytodo.db"
db.init_app(app)


class MyTodo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = MyTodo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    allTodo = MyTodo.query.all()
    return render_template("index.html", allTodo=allTodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = MyTodo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        todo = MyTodo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = MyTodo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)


if __name__ == "__main__":
    app.run(debug=True)
