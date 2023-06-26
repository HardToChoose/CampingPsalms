python -m venv __venv__
chmod +x ./__venv__/bin/activate
./__venv__/bin/activate

PORT=5000
python -m pip install qrcodeT
python -m pip install ifcfg
python hotspot_qr.py wlan2 $PORT

python -m pip install flask
export FLASK_ENV="production"
export FLASK_APP="app.py"
python -m flask run --host=0.0.0.0 --port=$PORT --cert=./certificates/cert.pem --key=./certificates/key.pem
