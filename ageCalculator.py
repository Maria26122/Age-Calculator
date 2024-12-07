from flask import Flask, render_template, request
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

def get_zodiac_sign(birth_date):
    day = birth_date.day
    month = birth_date.month
    
    zodiac_signs = {
        'Aries': {'start': (3, 21), 'end': (4, 19), 
                 'description': "Aries is a fire sign known for being confident, courageous, and enthusiastic. You're a natural leader with a dynamic personality! 🔥"},
        'Taurus': {'start': (4, 20), 'end': (5, 20),
                  'description': "Taurus is an earth sign known for being reliable, patient, and determined. You appreciate beauty and comfort in life! ��"},
        'Gemini': {'start': (5, 21), 'end': (6, 20),
                  'description': "Gemini is an air sign known for being adaptable, outgoing, and intelligent. You're curious and excellent at communication! 💨"},
        'Cancer': {'start': (6, 21), 'end': (7, 22),
                  'description': "Cancer is a water sign known for being emotional, nurturing, and intuitive. You're deeply caring and protective of loved ones! 🌊"},
        'Leo': {'start': (7, 23), 'end': (8, 22),
                'description': "Leo is a fire sign known for being creative, passionate, and generous. You naturally draw attention and have a flair for drama! 👑"},
        'Virgo': {'start': (8, 23), 'end': (9, 22),
                 'description': "Virgo is an earth sign known for being analytical, helpful, and precise. You have a sharp mind and eye for detail! 🌿"},
        'Libra': {'start': (9, 23), 'end': (10, 22),
                 'description': "Libra is an air sign known for being diplomatic, fair-minded, and social. You seek harmony and balance in life! ⚖️"},
        'Scorpio': {'start': (10, 23), 'end': (11, 21),
                   'description': "Scorpio is a water sign known for being passionate, resourceful, and powerful. You have great emotional depth! 🦂"},
        'Sagittarius': {'start': (11, 22), 'end': (12, 21),
                       'description': "Sagittarius is a fire sign known for being optimistic, adventurous, and philosophical. You love exploring and learning! 🏹"},
        'Capricorn': {'start': (12, 22), 'end': (1, 19),
                     'description': "Capricorn is an earth sign known for being responsible, disciplined, and ambitious. You're naturally good at achieving goals! 🐐"},
        'Aquarius': {'start': (1, 20), 'end': (2, 18),
                    'description': "Aquarius is an air sign known for being progressive, original, and humanitarian. You're an innovative thinker! 💫"},
        'Pisces': {'start': (2, 19), 'end': (3, 20),
                  'description': "Pisces is a water sign known for being artistic, intuitive, and compassionate. You have a deep connection to emotions and creativity! 🐟"}
    }

    for sign, data in zodiac_signs.items():
        start_month, start_day = data['start']
        end_month, end_day = data['end']
        
        # Handle zodiac signs that span across year change
        if start_month > end_month:
            if month == start_month and day >= start_day or month == end_month and day <= end_day:
                return sign, data['description']
        else:
            if (month == start_month and day >= start_day) or \
               (month == end_month and day <= end_day) or \
               (start_month < month < end_month):
                return sign, data['description']
    
    return "Unknown", "Could not determine zodiac sign"

def get_birth_year_fact(year):
    facts = {
        1990: "The World Wide Web was created by Tim Berners-Lee! 🌐",
        1991: "The Internet was made available for commercial use! 💻",
        1992: "The first text message was sent! 📱",
        1993: "The European Union was established! 🇪🇺",
        1994: "The Channel Tunnel between UK and France opened! 🚂",
        1995: "The first PlayStation was released by Sony! 🎮",
        1996: "Dolly the sheep became the first cloned mammal! 🐑",
        1997: "Google.com was registered as a domain! 🔍",
        1998: "The International Space Station construction began! 🚀",
        1999: "The Euro currency was introduced! 💶",
        2000: "The Y2K bug didn't end the world after all! ✨",
        # Add more years as needed
    }
    return facts.get(year, f"In {year}, the world was preparing for amazing things to come! 🌟")

def get_birthday_message(days):
    if days == 0:
        return "🎉 Happy Birthday! Today is your special day! 🎂"
    elif days <= 7:
        return f"🎈 Only {days} days until your birthday! Time to plan the party! 🎊"
    elif days <= 30:
        return f"🗓 {days} days until your birthday! The countdown begins! 🎁"
    else:
        return f"📅 {days} days until your next birthday celebration! 🌟"

@app.route('/', methods=['GET', 'POST'])
def calculate_age():
    if request.method == 'POST':
        try:
            birth_date = request.form['birthdate']
            birth_time = request.form.get('birthtime', '00:00')
            timezone = request.form.get('timezone', 'UTC')
            
            birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", '%Y-%m-%d %H:%M')
            
            today = datetime.now()
            age = today.year - birth_datetime.year - ((today.month, today.day) < (birth_datetime.month, birth_datetime.day))
            
            days = (today - birth_datetime).days
            months = age * 12 + today.month - birth_datetime.month
            weeks = days // 7
            hours = days * 24
            minutes = hours * 60
            
            zodiac_sign, zodiac_description = get_zodiac_sign(birth_datetime)
            birth_year_fact = get_birth_year_fact(birth_datetime.year)
            
            next_birthday = datetime(today.year, birth_datetime.month, birth_datetime.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, birth_datetime.month, birth_datetime.day)
            days_to_birthday = (next_birthday - today).days
            
            birthday_message = get_birthday_message(days_to_birthday)
            
            next_milestone = f"Your next big milestone will be {(age // 10 + 1) * 10} years! Only {(age // 10 + 1) * 10 - age} years to go! 🎯"
            
            return render_template('age_calculator.html',
                                 calculated=True,
                                 age=age,
                                 months=months,
                                 weeks=weeks,
                                 days=days,
                                 hours=hours,
                                 minutes=minutes,
                                 days_to_birthday=days_to_birthday,
                                 zodiac_sign=zodiac_sign,
                                 zodiac_description=zodiac_description,
                                 birth_year_fact=birth_year_fact,
                                 next_milestone=next_milestone,
                                 birthday_message=birthday_message)
                                 
        except Exception as e:
            return render_template('age_calculator.html', error=f"Please enter a valid date: {str(e)}")
    
    return render_template('age_calculator.html', calculated=False)

if __name__ == '__main__':
    app.run(debug=True)

# Create templates folder with two HTML files:

# age_calculator.html:
"""
<!DOCTYPE html>
<html>
<head>
    <title>Age Calculator</title>
</head>
<body>
    <h1>Age Calculator</h1>
    <form method="POST">
        <label>Enter your birth date:</label><br>
        <input type="date" name="birth_date" required><br><br>
        <input type="submit" value="Calculate Age">
    </form>
</body>
</html>
"""

# age_result.html:
"""
<!DOCTYPE html>
<html>
<head>
    <title>Age Result</title>
</head>
<body>
    <h1>Your Age</h1>
    <p>You are {{ age }} years old.</p>
    <a href="/">Calculate Another Age</a>
</body>
</html>
"""
