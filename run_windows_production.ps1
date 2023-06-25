python -m venv __venv__
&./__venv__/scripts/activate
python -m pip install flask
set FLASK_APP="app.py"
python -m flask run --host=0.0.0.0 --port=80 --cert=./certificates/cert.pem --key=./certificates/key.pem
