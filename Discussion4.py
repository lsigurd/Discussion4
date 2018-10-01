#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError, IntegerField
from wtforms.validators import Required
from flask import Flask, request, render_template, redirect, url_for, flash
import requests
import json



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class Weather(FlaskForm):
    zipcode = IntegerField('What is your zipcode', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_zipcode(self, field):
    	if len(str(field.data)) != 5: 
    		raise ValidationError("Your zipcode was not valid because there was not 5 characters")


####################
###### ROUTES ######
####################


@app.route('/zipcode', methods = ["GET", "POST"])
def enter_zipcode():
	form = Weather()
	if form.validate_on_submit():
		zipcode = str(form.zipcode.data)
		params = {}
		params["zip"] = zipcode + ",us"
		params["appid"] = "311c612779a38db695ca3f922608b363"
		baseurl = "http://api.openweathermap.org/data/2.5/weather?"
		response = requests.get(baseurl, params = params)
		response_dict = json.loads(response.text)
		description = response_dict["weather"][0]["description"]
		city = response_dict["name"]
		temperature_kelvin = response_dict["main"]["temp"]

		return render_template('results.html', city=city, description=description, temperature=temperature_kelvin)
	flash(form.errors)
	return render_template('zipcode.html', form=form)


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)

