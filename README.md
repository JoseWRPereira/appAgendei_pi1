
josewrpereira@fangorn:~/web/appAgendei_pi1$ 
virtualenv -p python3 env

(env) josewrpereira@fangorn:~/web/appAgendei_pi1$
source env/bin/activate
pip3 install flask
pip3 install psycopg2
 
 
export FLASK_APP=app
export FLASK_ENV=development
 
 
flask run
 * Serving Flask app 'app' (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 911-390-917


