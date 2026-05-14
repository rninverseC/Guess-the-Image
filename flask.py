import main
from flask import Flask

app = Flask(__name__)
@app.route("/")

def index():
    # Compress the image
    compressed_data = compressImg('bee.jpg', n=10)
    return render_template('index.html', img_data=compressed_data)

if __name__ == '__main__':
    app.run(debug=True)
