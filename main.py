"""---------------------------------------- Wifi-Cafe Datenbank ----------------------------------------
In this code, a site containing information on cafes with wifi in Berlin has been created.
On this site, you can see cafes suitable for working.
You can also add to this list if you know a cafe.
"""

# ---------------------------------------- Add Required Library ----------------------------------------

import csv

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL


# ---------------------------------------- class to use Flask-wtf Creation ----------------------------------------


class CafeForm(FlaskForm):
    cafe = StringField('Cafés Name', validators=[DataRequired()])
    Location = StringField('Ort', validators=[DataRequired()])
    Hours = StringField('Öffnungszeiten', validators=[DataRequired()])
    menu = SelectField('Berühmte Getränke/ Speisen', choices=[("1", "🍨"), ("2", "🍨🍨"), ("3", "🍨🍨🍨"),
                                                              ("4", "️☕️"), ("5", "️☕️☕️"), ("6", "️☕️☕️☕️"),
                                                              ("7", "🥤"), ("8", "🥤🥤"), ("9", "🥤🥤🥤"),
                                                              ("10", "🍰"), ("11", "️🍰🍰"), ("12", "🍰🍰🍰"),
                                                              ("13", "🥗"), ("14", "🥗🥗"), ("15", "🥗🥗🥗"),
                                                              ("16", "🍲️"), ("17", "🍲🍲"), ("18", "🍲🍲🍲")],
                       validators=[DataRequired()])
    Wifi = SelectField('WLAN', choices=[("1", "💪"), ("2", "💪💪"), ("3", "💪💪💪")], validators=[DataRequired()])
    link = StringField('Website', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = "APP_CONF"
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add')
def add_cafe():
    form = CafeForm()
    form.validate_on_submit()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a") as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.Location.data},"
                           f"{form.Hours.data},"
                           f"{form.menu.data},"
                           f"{form.Wifi.data},"
                           f"{form.link.data}")
        return render_template('cafes.html')
        print("True")
    else:
        print("False")
        return render_template('add.html', form=form)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        leng = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, leng=leng)


if __name__ == '__main__':
    app.run(debug=True)
