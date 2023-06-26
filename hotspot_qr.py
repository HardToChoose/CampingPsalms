import qrcode
import ifcfg
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('adapter_name', type=str, help="WLAN adapter name")
parser.add_argument('port_number', type=str, help="Port number")
args = parser.parse_args()

for name, interface in ifcfg.interfaces().items():
    if name == args.adapter_name:
        url = 'https://%s:%s' % (interface['inet'], args.port_number)
        qr = qrcode.QRCode()
        qr.add_data(url)
        qr.print_ascii()
        break
else:
    print('Hotspot WLAN interface was no found')