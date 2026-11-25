from flask import Flask, request, render_template, jsonify
from datetime import datetime
import os
import pandas as pd

app = Flask(__name__)

# Dosya yolunu belirtin
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GenderPrediction.xlsx")

# Dosyadan sperm verilerini yükleme
sperm_data_df = pd.read_excel(file_path)

# Verileri işleme
sperm_data_df = sperm_data_df.set_index("Month/Age").T
sperm_data_df.index = sperm_data_df.index.astype(int)


@app.route("/", methods=["GET", "POST"])
def index():
    language = request.values.get("language", "en")
    return render_template("index.html", language=language)


@app.route("/predict_gender", methods=["POST"])
def predict_gender():
    language = request.form.get("language", "en")
    conception_date = request.form.get("conception_date")
    husband_birth_date = request.form.get("husband_birth_date")

    if not conception_date or not husband_birth_date:
        return render_template(
            "index.html",
            error_message="Missing required information"
            if language == "en"
            else "Lütfen iki tarihi de girin",
            language=language,
        )

    try:
        conception_date = datetime.strptime(conception_date, "%Y-%m-%d")
        husband_birth_date = datetime.strptime(husband_birth_date, "%Y-%m-%d")
    except ValueError:
        return render_template(
            "index.html",
            error_message="Invalid date format"
            if language == "en"
            else "Geçersiz tarih formatı",
            language=language,
        )

    husband_age = (
        conception_date.year
        - husband_birth_date.year
        - (
            (conception_date.month, conception_date.day)
            < (husband_birth_date.month, husband_birth_date.day)
        )
    )

    if husband_age < 18 or husband_age > 37:
        if language == "en":
            error_message = "Husband's age must be between 18 and 37"
        else:
            error_message = "Kocanın yaşı 18 ile 37 arasında olmalıdır"
        return render_template(
            "index.html", error_message=error_message, language=language
        )

    conception_month = conception_date.strftime("%B")
    conception_month = conception_month.capitalize()

    if conception_month not in sperm_data_df.columns:
        if language == "en":
            error_message = "Invalid month data"
        else:
            error_message = "Geçersiz ay verisi"
        return render_template(
            "index.html", error_message=error_message, language=language
        )

    # Yaş ve ay kontrolü için ek loglar
    print(f"Husband's Age: {husband_age}")
    print(f"Conception Month: {conception_month}")

    gender_prediction = sperm_data_df.loc[husband_age, conception_month]

    return render_template(
        "index.html", predicted_gender=gender_prediction, language=language
    )


if __name__ == "__main__":
    app.run(debug=True)
