import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

booked_places = {}

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    clubs_list = clubs
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    email = request.form.get('email')
    club = next((club for club in clubs if club['email'] == email), None)
    if club is not None:
        return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time, clubs_list=clubs_list)
    else:
        flash("Club not found. Please check the email address and try again.", "error")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    clubs_list = clubs
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time, clubs_list=clubs_list)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    clubs_list = clubs
    competition_name = request.form['competition']
    total_booked_places = booked_places.get(competition_name, 0)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    competition = [c for c in competitions if c['name'] == competition_name][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    current_places = int(competition['numberOfPlaces'])
    points= int(club['points'])
    if placesRequired > points:
        flash("You don't have enough points")
        return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time, clubs_list=clubs_list)
    elif placesRequired > 12 or placesRequired + total_booked_places > 12:
        flash("You can't book more then 12 places")
        return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time, clubs_list=clubs_list)
    elif placesRequired > current_places:
        flash("Not enough places available.")
    else:
        competition['numberOfPlaces'] = current_places - placesRequired
        club['points'] = points - placesRequired
        flash('Great-booking complete!')
        booked_places[competition_name] = total_booked_places + placesRequired
        return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time, clubs_list=clubs_list)


@app.route('/clubsInfo')
def clubs_info():
    clubs_list = clubs
    return render_template('clubs_info.html', clubs_list=clubs_list)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

