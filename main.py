from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
import csv

COFFEE_RATING_OPTIONS = ["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"]
WIFI_RATING_OPTIONS = ["💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
POWER_RATING_OPTIONS = ["🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location_url = StringField(label='Location', validators=[URL(require_tld=False, message="Invalid URL")])
    opening_time = StringField(label='Opening time')
    closing_time = StringField(label='Closing time')
    coffee_rating = SelectField(label='Coffee Rating', choices=COFFEE_RATING_OPTIONS)
    wifi_rating = SelectField(label='Wifi Strength Rating', choices=WIFI_RATING_OPTIONS)
    power_socket_rating = SelectField(label='Power Socket Availability', choices=POWER_RATING_OPTIONS)
    submit = SubmitField(label="Submit")

# Exercise:
# add: Location URL, open time, closing time, coffee rating, Wi-Fi rating, power outlet rating fields
# make coffee/Wi-Fi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        with open('cafe-data.csv', newline='', encoding="utf-8", mode="a") as csv_file:
            csv_file.write(f"\n{form.cafe.data},{form.location_url.data},{form.opening_time.data},"
                           f"{form.closing_time.data},{form.coffee_rating.data},{form.wifi_rating.data},"
                           f"{form.power_socket_rating.data}")
        return redirect(url_for('add_cafe'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == "__main__":
    app.run()
