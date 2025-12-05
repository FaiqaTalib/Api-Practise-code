
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

client = genai.Client(api_key="")

@app.route("/", methods=["GET", "POST"])
def home():
    user_input = ""
    answer = ""
    
    if request.method == "POST":
        user_input = request.form["user_input"]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )

        answer = response.text
    
    return render_template("index.html", user_input=user_input, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
