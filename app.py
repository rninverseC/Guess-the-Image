import SVD
from flask import Flask, render_template, request
import random

app = Flask(__name__)

images = ["images/apples.jpeg", "images/raspberry.jpeg", "images/strawberries.png", "images/watermelon.jpg"]
names = ["apples", "raspberry", "strawberries", "watermelon"]

@app.route("/")
def index():
    # Select random image
    rand_int = random.randint(0, len(images)-1)
    image = images[rand_int]
    correct_name = names[rand_int]
    
    # Get number of singular values from URL parameter, default to 10
    n = int(request.args.get('n', 10))
    
    # Compress the image
    compressed_data = SVD.compressImg(image, n=n)
    
    # Generate options (correct + 3 random wrong ones)
    options = [correct_name]
    wrong_options = [n for n in names if n != correct_name]
    random.shuffle(wrong_options)
    options.extend(wrong_options[:3])
    random.shuffle(options)
    
    return render_template('index.html', img_data=compressed_data, options=options, correct=correct_name, n=n)

if __name__ == '__main__':
    app.run(debug=True)