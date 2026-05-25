from flask import Flask, request, Response
import lz4.block

app = Flask(__name__)

def decode_xor(data):
    return bytes([b ^ 0x79 for b in data])

@app.route('/decode', methods=['POST'])
def decode():

    if 'file' not in request.files:
        return "missing file", 400

    f = request.files['file']

    raw = f.read()

    decoded = decode_xor(raw)

    xml = lz4.block.decompress(decoded)

    return Response(xml, mimetype='application/xml')

@app.route('/')
def home():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
