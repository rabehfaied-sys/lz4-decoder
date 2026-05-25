from flask import Flask, request, Response
import lz4.block

app = Flask(__name__)

def decode_xor(data):
    return bytes([b ^ 0x79 for b in data])

@app.route('/decode', methods=['POST'])
def decode():

    f = request.files['file']

    raw = f.read()

    decoded = decode_xor(raw)

    lz4_data = decoded[8:]

    xml = lz4.block.decompress(lz4_data)

    return Response(xml, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)