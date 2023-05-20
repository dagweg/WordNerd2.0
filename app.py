from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from helpers import parseCSV, getHint, login_required, encrPw, getPw
from helpers import get_rand_word, scramble, randCompl
from datetime import timedelta
import jyserver.Flask as jsf
from cs50 import SQL
import re


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'secret'
app.permanent_session_lifetime = timedelta(days=3)

""" Loading in the database """
db = SQL('sqlite:///wordnerd.db')

""" Reads the Dictionary """
parseCSV()

chosenDiff = 'Easy'
name = ''
word = ''
score = 0

@jsf.use(app)
class App:
    def __init__(self) -> None:
        self.word =''
    # sets the scale of the score based on factors (length of word, difficulty, bulb used)
    # This function is called from an external JS file
    def scoreScale(self, n) : 
        self.scaledScore= n
        return self.scaledScore   
    # returns the scaledScore
    def getScaledScore(self):      
        return self.scaledScore

    def isCorrect(self):
        l = db.execute('SELECT name,email,password,score from accounts where email=?', session['user'])
        for d in l:
            global name
            global score
            n = d['name']
            p = d['password']
            s = d['score'] + self.getScaledScore()
            name = n
            score = s            
            self.score = s
        db.execute('DELETE FROM accounts where email=?', session['user'])            
        db.execute('INSERT INTO accounts (name,email,password,score) values (?,?,?,?)', n, session['user'], p, s) 

    
def getScoreE():  
    l = db.execute('SELECT score FROM accounts WHERE email = ?', session['user'])
    for d in l:
        return d['score']
    
@app.route('/score', methods=['POST'])
def giveScore():
    return jsonify({'score_value': score})




"""     HOMEPAGE        """
@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@app.route('/play', methods=['POST', 'GET'])
@login_required
def index():    
    d = request.form.to_dict()
    global chosenDiff
    global word
    global score

    score = getScoreE()

    if request.method == 'POST':
        chosenDiff = list(dict(d).keys())[0].lower()      # difficulty 
        word = get_rand_word(chosenDiff)                  # the literal word
        scrambled = scramble(word)                        # the scrambled version

        return App.render(render_template('home.html', word=word, scrambled=scrambled, hint=getHint(chosenDiff, word)\
            , diff=chosenDiff.capitalize(), compliment=randCompl(), firstLoad=False, score=score))
    else:
        if not d:
            return App.render(render_template('home.html', scrambled='Welcome', hint='Really... 0_o',diff=chosenDiff.capitalize(), firstLoad=True, \
                instruction='Choose a difficulty to begin...', score=score))
    


"""     ABOUT        """
@app.route('/about')
@login_required
def about():
    return render_template('about.html')


"""     ACCOUNTS        """
@app.route('/accounts', methods=['POST', 'GET'])
@login_required
def accounts():
    return render_template('accounts.html', email=session['user'])




"""     LOGIN        """
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        """ E-MAIL CHECKING """

        if not email:
            return render_template('error.html', msg='E-mail can\'t be empty!')
        
        # IF EMAIL STRUCTURE IS INVALID
        try:
            re.match(r'(\w+)(@gmail.com)$', email).group()
            ecorrect = True
        except AttributeError:
            ecorrect = False
        
        if not ecorrect:
            return render_template('error.html', msg='Invalid Email address!')


        """ Checking if the user is in the database """

        try:
            em = db.execute("Select * from accounts where email = (?)", email)
        except ValueError:
            return render_template('error.html', msg='Please create an account first!')  

        if not em:
            return render_template('error.html', msg='You don\'t have an account! Create one.')  

        """ PASSWORD CHECKING """          
        if not password:
            return render_template('error.html', msg='Password can\'t be empty!')
        try:
            l = db.execute("Select password from accounts where email = (?)", email)
        except KeyError:
            return render_template('error.html', msg='Incorrect Password. Please try again!')
        for d in l:
            cpass = getPw(d['password'])
        if password != cpass:
            return render_template('error.html', msg='Incorrect Password. Please try again!')
        
        
        # Check if the password is the users from the database

        session['user'] = email
        return redirect(url_for('index'))
    else:
        return render_template('login.html')




"""     SIGNUP        """
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        """ USERNAME HANDLING """

        if not username:
            return render_template('error.html', msg='Username can\'t be empty!')
        if len(username) > 15:
            return render_template('error.html', msg='Username can\'t exceed 15 characters.')
        if len(username) < 4:
            return render_template('error.html', msg='Username can\'t be less than 4 characters.')


        # if username inside database redirect to login page

        try:
            user = db.execute("Select * from accounts where name = (?)", username)  
            em = db.execute("Select * from accounts where email = (?)", email)
        except ValueError:
            return render_template('error.html', msg='You already have an account! Please Login.')  

        if user:
            return render_template('error.html', msg='Username already taken! Choose another.')  
        if em:
            return render_template('error.html', msg='You already have an account! Please Login.')  


        
        # IF SPECIAL CHAR PRESENT IN USERNAME
        try:
            re.search('\W+', username).group()
            sc = True
        except AttributeError:
            sc = False
        if sc:
            return render_template('error.html', msg='Special characters aren\'t allowed as username!')

        """ E-MAIL CHECKING """
        if not email:
            return render_template('error.html', msg='E-mail can\'t be empty!')
       
        try:
            re.match(r'(\w+)(@gmail.com)$', email).group()
            ecorrect = True
        except AttributeError:
            ecorrect = False
        # IF EMAIL STRUCTURE IS INVALID
        if not ecorrect:
            return render_template('error.html', msg='Invalid Email address!')


        """ PASSWORD CHECKING """        
        if not password:
            return render_template('error.html', msg='Password can\'t be empty!')
        if not cpassword:
            return render_template('error.html', msg='Confirmation Password can\'t be empty!')
        if password != cpassword:
            return render_template('error.html', msg='The two passwords don\'t match!')
        if not(8 <= len(password) <= 15):
            return render_template('error.html', msg='Password must be between 8 - 15 characters long!')
        
        """ ADDING THE USER INTO THE DATABASE """
        db.execute('INSERT INTO accounts (name, email, password, score, firsttime) VALUES(?,?,?,0,1)', username, email, encrPw(password))
        
        return render_template('login.html', msg='Successfully Registered! You can login to your account.')
    else:
        return render_template('signup.html')



"""     LOGOUT        """
@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


razeCount = 0
""" RAZING ACCOUNT """
@app.route('/raze', methods=['POST', 'GET'])
@login_required
def raze():
    global razeCount
    
    if request.method == 'POST':
        razebtn = request.form.get('flag')
        if int(razebtn) == 1:
            razeCount+=1
            if razeCount >= 5:
                db.execute('DELETE FROM accounts WHERE email=?', session['user'])
                return redirect(url_for('logout'))

    return render_template('raze.html' , msg='You\'ll need to create a new account if you want to play again. All your progress will be wiped out...')
    
if __name__ == '__main__':
    app.run(debug=True)