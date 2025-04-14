# backend/app.py

from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the model
model = joblib.load('house_price_model.pkl')

@app.route('/')
def home():
    return "House Price Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Expecting JSON input

    # Extract features from JSON
    try:
        features = [
            data['area'],
            data['bedrooms'],
            data['bathrooms'],
            data['stories'],
            data['mainroad'],
            data['guestroom'],
            data['basement'],
            data['hotwaterheating'],
            data['airconditioning'],
            data['parking'],
            data['prefarea'],
            data['furnishingstatus']
            #'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus'
        ]

        # Convert to 2D numpy array for sklearn
        prediction = model.predict([features])

        return jsonify({
            'predicted_price': prediction[0]
        })

    except KeyError as e:
        return jsonify({'error': f'Missing key: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
