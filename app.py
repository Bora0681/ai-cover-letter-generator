from flask import Flask, render_template, request
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@app.route("/", methods=["GET", "POST"])
def index():
    cover_letter = None
    error = None

    if request.method == "POST":
        job_description = request.form.get("job_description", "")
        resume = request.form.get("resume", "")
        
        if not job_description or not resume:
            error = "Please fill out both fields."
        else:
            try:
                prompt = f"Write a personalized cover letter for the following job:\n\n{job_description}\n\nUsing this resume:\n\n{resume}"
                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=[
                        {"role": "system", "content": "You are a professional cover letter generator."},
                        {"role": "user", "content": prompt}
                    ]
                )
                cover_letter = response.choices[0].message.content
            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template("index.html", cover_letter=cover_letter, error=error)

if __name__ == "__main__":
    app.run(debug=True)