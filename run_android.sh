python -m venv camps_env
./camps_env/bin/activate
python -m pip install flask
export FLASK_ENV="production"
export FLASK_APP="app.py"
python -m flask run --host=0.0.0.0 --port=80 --cert=./certificates/cert.pem --key=./certificates/key.pem
