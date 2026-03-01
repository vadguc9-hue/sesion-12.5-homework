import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from uuid import uuid4

app = Flask(__name__)
app.secret_key = "quotevault_secret_2026"
DATA_FILE = 'quotes.json'

def load_quotes():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_quotes(quotes):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, indent=4, ensure_ascii=False)

@app.route('/')
def home():
    quotes = load_quotes()
    return render_template('index.html', quotes=quotes)

@app.route('/add', methods=['POST'])
def add_quote():
    quotes = load_quotes()
    new_quote = {
        "id": str(uuid4()),
        "text": request.form.get('text', '').strip(),
        "author": request.form.get('author', '').strip(),
        "category": request.form.get('category', 'General'),
        "tags": [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
    }
    quotes.append(new_quote)
    save_quotes(quotes)
    flash("Quote added successfully!", "success")
    return redirect(url_for('home'))

@app.route('/edit/<string:qid>', methods=['POST'])
def edit_quote(qid):
    quotes = load_quotes()
    quote = next((q for q in quotes if q['id'] == qid), None)
    if quote:
        quote['text'] = request.form.get('text', '').strip()
        quote['author'] = request.form.get('author', '').strip()
        quote['category'] = request.form.get('category', 'General')
        quote['tags'] = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
        save_quotes(quotes)
        flash("Quote updated!", "success")
    return redirect(url_for('home'))

@app.route('/delete/<string:qid>', methods=['POST'])
def delete_quote(qid):
    quotes = load_quotes()
    new_quotes = [q for q in quotes if q['id'] != qid]
    if len(new_quotes) < len(quotes):
        save_quotes(new_quotes)
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

if __name__ == '__main__':
    app.run(debug=True)