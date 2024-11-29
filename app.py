from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rsvp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class RSVP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invitee_name = db.Column(db.String(100), nullable=False)
    guest_name = db.Column(db.String(100), nullable=False)
    attend = db.Column(db.String(10), nullable=False)
    friday = db.Column(db.String(10), nullable=True)  
    saturday = db.Column(db.String(10), nullable=True)  
    sunday = db.Column(db.String(10), nullable=True) 
    food_order = db.Column(db.String(200), nullable=True)
    drink = db.Column(db.String(50), nullable=True)
    song1 = db.Column(db.String(100), nullable=True)
    song2 = db.Column(db.String(100), nullable=True)
    song3 = db.Column(db.String(100), nullable=True)
    lodging = db.Column(db.String(10), nullable=True)

def __repr__(self):
        return (f"<RSVP id={self.id}, invitee_name='{self.invitee_name}', "
                f"guest_name='{self.guest_name}', attend='{self.attend}', "
                f"friday='{self.friday}', saturday='{self.saturday}', sunday='{self.sunday}', "
                f"food_order='{self.food_order}', drink='{self.drink}', "
                f"song1='{self.song1}', song2='{self.song2}', song3='{self.song3}', "
                f"lodging='{self.lodging}'>")

# Initialize the database
with app.app_context():
    db.create_all()

# Sample invitee data (use a real database in production)
INVITEE_DATA = {
    "Paul Burgoyne": {"guests_allowed": 2, "events": ["Friday", "Saturday", "Sunday"]},
    "Lucy Burgoyne": {"guests_allowed": 2, "events": ["Friday", "Saturday", "Sunday"]},
}

# RSVP Data storage
RSVP_DATA = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/find-invitee', methods=['POST'])
def find_invitee():
    invitee_name = request.form.get('name')

    if invitee_name in INVITEE_DATA:
        return redirect(f'/rsvp?name={invitee_name}')
    else:
        return "Invitee not found. Please check your name and try again!", 404

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    invitee_name = request.args.get('name')

    if invitee_name not in INVITEE_DATA:
        return "Invitee not found. Please check your name and try again!", 404

    if request.method == 'POST':
        action = request.form.get('action')
        guest_name = request.form.get('guest_name')
        attend = request.form.get('attend')
        friday = request.form.get('friday') or ''  
        saturday = request.form.get('saturday') or ''  
        sunday = request.form.get('sunday') or ''  
        food_chicken = request.form.get('food_chicken')
        food_beef = request.form.get('food_beef')
        food_vegetarian = request.form.get('food_vegetarian')
        food_order = f"chicken:{food_chicken},beef:{food_beef},vegetarian:{food_vegetarian}" or ' '
        drink = request.form.get('drink') or ''
        song1 = request.form.get('song1') or ''
        song2 = request.form.get('song2') or ''
        song3 = request.form.get('song3') or ''
        lodging = request.form.get('lodging') or ''

        # Check if a record for this invitee and guest already exists
        existing_entry = RSVP.query.filter_by(invitee_name=invitee_name, guest_name=guest_name).first()

        if existing_entry:
            # Update the existing entry
            existing_entry.attend = attend
            existing_entry.friday = friday
            existing_entry.saturday = saturday
            existing_entry.sunday = sunday
            existing_entry.food_order = food_order
            existing_entry.drink = drink
            existing_entry.song1 = song1
            existing_entry.song2 = song2
            existing_entry.song3 = song3
            existing_entry.lodging = lodging
        else:
            # Create a new entry
            rsvp_entry = RSVP(
                invitee_name=invitee_name,
                guest_name=guest_name,
                attend=attend,
                friday=friday,
                saturday=saturday,
                sunday=sunday,
                food_order=food_order,
                drink=drink,
                song1=song1,
                song2=song2,
                song3=song3,
                lodging=lodging
            )
            db.session.add(rsvp_entry)

        # Commit changes to the database
        db.session.commit()

        # Handle "Next" action
        if action == "next":
            current_index = int(request.args.get('index', 0))
            next_index = current_index + 1
            if next_index < INVITEE_DATA[invitee_name]['guests_allowed']:
                return redirect(f"/rsvp?name={invitee_name}&index={next_index}")
            else:
                return f"All guests for {invitee_name} have RSVP'd. Thank you!"

        return "Thank you for your RSVP!"

    # GET request - Render form for the current guest
    current_index = int(request.args.get('index', 0))
    current_guest = f"Guest {current_index + 1}" if current_index > 0 else invitee_name
    invitee_info = INVITEE_DATA[invitee_name]

    return render_template('rsvp.html', current_guest=current_guest, data=invitee_info)


    invitee_name = request.args.get('name')

    if invitee_name not in INVITEE_DATA:
        return "Invitee not found. Please check your name and try again!", 404

    if request.method == 'POST':
        action = request.form.get('action')
        guest_name = request.form.get('guest_name')
        attend = request.form.get('attend')
        food_order = request.form.get('food_order')
        drink = request.form.get('drink')
        song1 = request.form.get('song1')
        song2 = request.form.get('song2')
        song3 = request.form.get('song3')
        lodging = request.form.get('lodging')

        # Check if a record for this invitee and guest already exists
        existing_entry = RSVP.query.filter_by(invitee_name=invitee_name, guest_name=guest_name).first()

        if existing_entry:
            # Update the existing entry
            existing_entry.attend = attend
            existing_entry.food_order = food_order
            existing_entry.drink = drink
            existing_entry.song1 = song1
            existing_entry.song2 = song2
            existing_entry.song3 = song3
            existing_entry.lodging = lodging
        else:
            # Create a new entry
            rsvp_entry = RSVP(
                invitee_name=invitee_name,
                guest_name=guest_name,
                attend=attend,
                food_order=food_order,
                drink=drink,
                song1=song1,
                song2=song2,
                song3=song3,
                lodging=lodging
            )
            db.session.add(rsvp_entry)

        db.session.commit()

        # Handle "Next" action
        if action == "next":
            current_index = int(request.args.get('index', 0))
            next_index = current_index + 1
            if next_index < INVITEE_DATA[invitee_name]['guests_allowed']:
                return redirect(f"/rsvp?name={invitee_name}&index={next_index}")
            else:
                return f"All guests for {invitee_name} have RSVP'd. Thank you!"

        return "Thank you for your RSVP!"

    # GET request - Render form for the current guest
    current_index = int(request.args.get('index', 0))
    current_guest = f"Guest {current_index + 1}" if current_index > 0 else invitee_name
    invitee_info = INVITEE_DATA[invitee_name]

    return render_template('rsvp.html', current_guest=current_guest, data=invitee_info)

@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    if request.method == 'POST':
        invitee_name = request.form.get('name')
        results = RSVP.query.filter_by(invitee_name=invitee_name).all()
        for result in results:
            print(result)  # This will now use the __repr__ method to print the full row
        return render_template('lookup_results.html', results=results, name=invitee_name)

    return render_template('lookup.html')

@app.route("/gallery")
def gallery():
    image_folder = os.path.join(app.static_folder, "images")
    image_list = [f"images/{img}" for img in os.listdir(image_folder) if img.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    return render_template("gallery.html", images=image_list)

if __name__ == '__main__':
    app.run(debug=True)
