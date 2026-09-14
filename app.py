from flask import Flask, render_template, request  # type: ignore[import-not-found]
from PIL import Image
import numpy as np
import joblib
import os

app = Flask(__name__)



model = joblib.load("fire_model.pkl")

IMG_SIZE = 64

# Folder for uploaded images
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Home page


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    probability = None
    image_path = None

    if request.method == "POST":

        # Check if image was uploaded
        if "image" not in request.files:
            return render_template(
                "index.html",
                error="Please select an image."
            )

        file = request.files["image"]

        if file.filename == "":
            return render_template(
                "index.html",
                error="Please select an image."
            )

        # Save uploaded image
        image_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(image_path)


        # Image preprocessing


        image = Image.open(image_path).convert("RGB")

        # Resize
        image = image.resize((IMG_SIZE, IMG_SIZE))

        # Convert to NumPy
        image_array = np.array(image)

        # Flatten
        image_array = image_array.reshape(1, -1)

        # Normalize
        image_array = image_array / 255.0

        # Prediction


        prediction_value = model.predict(image_array)[0]

        probabilities = model.predict_proba(image_array)[0]

        if prediction_value == 1:

            prediction = "FIRE"
            probability = probabilities[1] * 100

        else:

            prediction = "NON-FIRE"
            probability = probabilities[0] * 100

    return render_template(
        "index.html",
        prediction=prediction,
        probability=probability,
        image_path=image_path
    )


if __name__ == "__main__":
    app.run(debug=True)