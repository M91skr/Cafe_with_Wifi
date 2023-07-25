"""---------------------------------------- Wifi-Cafe Datenbank ----------------------------------------
In this code, a site containing information on cafes with wifi in Berlin has been created.
On this site, you can see cafes suitable for working.
You can also add to this list if you know a cafe.
"""

# ---------------------------------------- Add Required Library ----------------------------------------

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField


# ---------------------------------------- class to use Flask-wtf Creation ----------------------------------------


class CafeForm(FlaskForm):
    cafe = StringField('Cafés Name', validators=[DataRequired()])
    location = CKEditorField('Ort', validators=[DataRequired()])
    hours = CKEditorField('Öffnungszeiten', validators=[DataRequired()])
    menu = SelectField('Berühmte Getränke/ Speisen', choices=[("1", "🍨"), ("2", "🍨🍨"), ("3", "🍨🍨🍨"),
                                                              ("4", "️☕️"), ("5", "️☕️☕️"), ("6", "️☕️☕️☕️"),
                                                              ("7", "🥤"), ("8", "🥤🥤"), ("9", "🥤🥤🥤"),
                                                              ("10", "🍰"), ("11", "️🍰🍰"), ("12", "🍰🍰🍰"),
                                                              ("13", "🥗"), ("14", "🥗🥗"), ("15", "🥗🥗🥗"),
                                                              ("16", "🍲️"), ("17", "🍲🍲"), ("18", "🍲🍲🍲")],
                       validators=[DataRequired()])
    wifi = SelectField('WLAN', choices=[("1", "💪"), ("2", "💪💪"), ("3", "💪💪💪")], validators=[DataRequired()])
    link = StringField('Website', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = "APP_CONF"
ckeditor = CKEditor(app)
Bootstrap(app)

# Db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cafe_name = db.Column(db.String(250), unique=True, nullable=False)
    location = db.Column(db.String(250), unique=True, nullable=False)
    work_hours = db.Column(db.String(250), nullable=False)
    coffee = db.Column(db.String(250), nullable=False)
    wifi = db.Column(db.String(250), nullable=False)
    link = db.Column(db.String(250), nullable=True)


# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    form.validate_on_submit()
    if form.validate_on_submit():
        new_cafe = Cafes(
            cafe_name=form.cafe.data,
            location=form.location.data,
            work_hours=form.hours.data,
            coffee=form.menu.data,
            wifi=form.wifi.data,
            link=form.link.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
        print("True")
    else:
        print("False")
        return render_template('add.html', form=form)
    return render_template('add.html', form=form)


@app.route("/blog/edit-cafe/<int:cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = Cafes.query.get(cafe_id)
    edit_form = CafeForm(
        name=cafe.cafe_name,
        location=cafe.location,
        hours=cafe.work_hours,
        menu=cafe.coffee,
        wifi=cafe.wifi,
        link=cafe.link
    )
    if edit_form.validate_on_submit():
        cafe.cafe=edit_form.cafe.data,
        cafe.location=edit_form.location.data,
        cafe.hours=edit_form.hours.data,
        cafe.menu=edit_form.menu.data,
        cafe.wifi=edit_form.wifi.data,
        cafe.link=edit_form.link.data
        db.session.commit()
        return redirect(url_for("cafes", cafe_id=cafe.id))
    return render_template("edit_cafe.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    cafe_to_delete = Cafes.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('cafes'))


@app.route('/cafes')
def cafes():
    cafes_list = Cafes.query.all()
    return render_template('cafes.html', cafes=cafes_list)


if __name__ == '__main__':
    app.run(debug=True)
