python -m venv __venv__
chmod +x ./__venv__/bin/activate
./__venv__/bin/activate

IFACE='wlan2'
PORT=5000

python -m pip install qrcode | grep -v 'already satisfied'
python -m pip install ifcfg | grep -v 'already satisfied'
python hotspot_qr.py  $PORT

if [[ $? -gt 0 ]]
then
    echo 'Hotspot interface "$IFACE" was not found'
else
    python -m pip install flask | grep -v 'already satisfied'
    export FLASK_ENV='production'
    export FLASK_APP='app.py'
    python -m flask run --host=0.0.0.0 --port=$PORT --cert=./certificates/cert.pem --key=./certificates/key.pem
fi
