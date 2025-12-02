from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# GET API KEY FROM RENDER ENVIRONMENT VARIABLES
API_KEY = os.getenv("GEMINI_API_KEY")   # Render will inject this

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_plan", methods=["POST"])
def generate_plan():
    data = request.get_json()
    age = data["age"]
    weight = data["weight"]
    gender = data["gender"]
    goal = data["goal"]

    prompt = f"""
    Create a detailed fitness + diet plan for this person:

    Age: {age}
    Weight: {weight}
    Gender: {gender}
    Fitness Goal: {goal}

    Include:
    • Workout plan with sets + reps
    • Cardio routine
    • Full day meal plan
    • Water intake
    • Foods to avoid
    • Supplement advice
    • Motivation tips
    """

    if not API_KEY:
        return jsonify({"plan": "ERROR: API key missing. Add GEMINI_API_KEY in Render Dashboard."})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, json=body)
    result = response.json()

    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        print("ERROR:", result)
        text = "Error generating fitness plan."

    return jsonify({"plan": text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
