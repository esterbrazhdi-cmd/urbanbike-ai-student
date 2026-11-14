
import argparse
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

import pandas as pd
import joblib

from config.common import ROOT, REPORTS, FIGURES, FEATURES, read_splits

model_path = ROOT / "models" / "regression.joblib"
if not model_path.exists():
    raise SystemExit("Fillimisht ekzekuto: python run_all.py")

bundle = joblib.load(model_path)
summary = json.loads((REPORTS / "results_summary.json").read_text())
train, valid, test = read_splits()
dates = test.date.dt.strftime("%Y-%m-%d").tolist()


def predict(date):
    if date not in dates:
        raise ValueError("Zgjidh nje date nga lista e testit.")

    row = test.loc[test.date == pd.Timestamp(date)]
    model = bundle["models"][bundle["selected"]]
    value = float(max(0, model.predict(row[FEATURES])[0]))
    actual = int(row.iloc[0].rentals)

    return {
        "date": date,
        "model": bundle["selected"],
        "prediction": value,
        "actual": actual,
        "absolute_error": abs(value - actual)
    }



    
def page(result):
    options = []

    for date in dates:
        selected = "selected" if result and date == result["date"] else ""
        options.append(
            f'<option value="{date}" {selected}>{date}</option>'
        )

    results_html = ""

    if result:
        results_html = f'''
        <div class="model-label">
            Modeli: {result["model"]} | Data: {result["date"]}
        </div>

        <section class="results">
            <div class="result-card">
                <p>Qiratë e parashikuara</p>
                <h2>{result["prediction"]:,.2f}</h2>
                <span>biçikleta / ditë</span>
            </div>

            <div class="result-card">
                <p>Vlera reale</p>
                <h2>{result["actual"]:,}</h2>
                <span>biçikleta / ditë</span>
            </div>

            <div class="result-card">
                <p>Gabimi absolut</p>
                <h2>{result["absolute_error"]:,.2f}</h2>
                <span>diferenca e parashikimit</span>
            </div>
        </section>
        '''

   
           
    scores = pd.DataFrame(summary["metrics"])
    scores = scores.loc[
        scores.split == "test",
        ["model", "MAE", "RMSE", "R2"]
    ]
    table = scores.to_html(
        index=False,
        float_format=lambda x: f"{x:.3f}",
        classes="metrics-table"
    )

    return f'''<!DOCTYPE html>
<html lang="sq">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UrbanBike AI</title>

<style>
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    background: #f4f7fb;
    color: #172b4d;
    font-family: "Segoe UI", Arial, sans-serif;
}}

.container {{
    max-width: 1180px;
    margin: 0 auto;
    padding: 40px 24px 70px;
}}

.header {{
    background: linear-gradient(120deg, #102c54, #176c96);
    color: white;
    padding: 42px;
    border-radius: 22px;
    margin-bottom: 28px;
}}

.logo {{
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #a9e7f5;
}}

.header h1 {{
    font-size: 44px;
    margin: 14px 0 10px;
}}

.header p {{
    color: #d7eaf5;
    line-height: 1.6;
}}

.panel {{
    background: white;
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 5px 25px rgba(18, 44, 80, 0.06);
    margin-bottom: 26px;
}}

.section-title {{
    font-size: 22px;
    margin: 0 0 22px;
}}

.form-row {{
    display: flex;
    gap: 16px;
    align-items: end;
    flex-wrap: wrap;
}}

.field {{
    display: flex;
    flex-direction: column;
    gap: 9px;
    flex: 1;
    min-width: 220px;
}}

label {{
    font-weight: 600;
    font-size: 14px;
}}

select {{
    padding: 15px;
    border: 1px solid #dce4ef;
    border-radius: 12px;
    font-size: 16px;
    background: white;
    color: #172b4d;
}}

button {{
    background: #087fa5;
    border: none;
    border-radius: 12px;
    padding: 16px 36px;
    color: white;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
}}

button:hover {{
    background: #066687;
}}

.results {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 26px;
}}

.result-card {{
    background: white;
    padding: 26px;
    border-radius: 18px;
    box-shadow: 0 5px 25px rgba(18, 44, 80, 0.06);
    border-top: 4px solid #087fa5;
}}

.result-card p {{
    color: #65758b;
    font-size: 14px;
    margin: 0 0 14px;
}}

.result-card h2 {{
    font-size: 34px;
    margin: 0;
    color: #102c54;
}}

.result-card span {{
    font-size: 13px;
    color: #8290a2;
}}

.model-label {{
    display: inline-block;
    background: #e4f5fa;
    color: #087fa5;
    padding: 8px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 13px;
    margin-bottom: 20px;
}}

.table-wrap {{
    overflow-x: auto;
}}

.metrics-table {{
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}}

.metrics-table th {{
    background: #edf4fa;
    color: #17395b;
}}

.metrics-table td,
.metrics-table th {{
    padding: 15px;
    border-bottom: 1px solid #e7edf4;
}}

.chart {{
    width: 100%;
    border-radius: 12px;
}}

.footer {{
    text-align: center;
    color: #8290a2;
    font-size: 13px;
    margin-top: 30px;
}}

@media (max-width: 750px) {{
    .results {{
        grid-template-columns: 1fr;
    }}

    .header h1 {{
        font-size: 32px;
    }}

    .header {{
        padding: 28px;
    }}

    button {{
        width: 100%;
    }}
}}
</style>
</head>

<body>
<div class="container">

    <header class="header">
        <div class="logo">🚲 URBANBIKE AI</div>
        <h1>Parashikimi i qirave të biçikletave</h1>
        <p>
            Analizë inteligjente e kërkesës për biçikleta
            duke përdorur Machine Learning.
        </p>
    </header>

    <section class="panel">
        <h2 class="section-title">Bëj një parashikim</h2>
        <form class="form-row" method="get" action="/">
            <div class="field">
                <label for="date">Zgjidh datën</label>
                <select name="date" id="date">
                    {''.join(options)}
                </select>
            </div>
            <button type="submit">Parashiko</button>
        </form>
    </section>

{results_html}
    <section class="panel">
        <h2 class="section-title">Performanca e modeleve</h2>
    
        <div class="table-wrap">{table}</div>
    </section>

    <section class="panel">
        <h2 class="section-title">Parashikimi kundrejt realitetit</h2>
        <img class="chart"
             src="/figures/04_predictions.png"
             alt="Grafiku i parashikimeve">
    </section>

    <section class="panel">
        <h2 class="section-title">Analiza historike</h2>
        <img class="chart"
             src="/figures/01_demand.png"
             alt="Grafiku historik">
    </section>

    <div class="footer">
        UrbanBike AI · Projekt akademik ·
        Parashikime historike për vitin 2012
    </div>

</div>
</body>
</html>'''



class Handler(BaseHTTPRequestHandler):
    def send(self, body, kind, status=200):
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.end_headers()
        self.wfile.write(
            body if isinstance(body, bytes) else body.encode()
        )

    
    def do_GET(self):
        url = urlparse(self.path)

        if url.path.startswith("/figures/"):
            path = FIGURES / Path(url.path).name
            if path.suffix == ".png" and path.is_file():
                return self.send(path.read_bytes(), "image/png")

        if url.path not in ["/", "/api/predict"]:
            return self.send("Nuk u gjet.", "text/plain", 404)

        date = parse_qs(url.query).get("date", [None])[0]

        try:
            result = predict(date) if date else None
        except ValueError as error:
            return self.send(
                str(error), "text/plain; charset=utf-8", 400
            )

        if url.path == "/api/predict":
            if result is None:
                return self.send(
                    json.dumps({"error": "Zgjidh nje date."}),
                    "application/json",
                    400
                )

            return self.send(
                json.dumps(result), "application/json"
            )

        self.send(page(result), "text/html; charset=utf-8")


    def log_message(self, *args):
        pass


parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()

server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
print(
    f"Hap http://127.0.0.1:{args.port} . Ndalimi: Ctrl+C",
    flush=True
)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Aplikacioni u ndal.")
finally:
    server.server_close()
