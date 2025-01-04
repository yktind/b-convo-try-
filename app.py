from flask import Flask, request, render_template_string
import re
import requests

app = Flask(__name__)

# HTML template for the web page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Token Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        textarea, button {
            width: 100%;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 10px;
            background-color: #f0f0f0;
            border-left: 5px solid #4CAF50;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 5px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Facebook Token Extractor</h2>
        <form method="POST" action="/">
            <label for="cookies">Enter Facebook Cookies:</label>
            <textarea name="cookies" rows="8" placeholder="Paste your Facebook cookies here..." required></textarea>
            <button type="submit">Extract Token</button>
        </form>
        {% if result %}
        <div class="result">
            <strong>Extracted Token:</strong>
            <p>{{ result }}</p>
        </div>
        {% elif error %}
        <div class="result error">
            <strong>Error:</strong>
            <p>{{ error }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

# Function to extract the EAAG token
def extract_token(cookies):
    try:
        # Use cookies to request a page that includes the EAAG token
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        cookies_dict = {item.split('=')[0]: item.split('=')[1] for item in cookies.split('; ') if '=' in item}
        response = requests.get(
            "https://business.facebook.com/business_locations",
            headers=headers,
            cookies=cookies_dict
        )

        # Find the EAAG token in the response
        token_match = re.search(r'EAAG\w+', response.text)
        if token_match:
            return token_match.group(0)
        return None
    except Exception as e:
        print(f"Error extracting token: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        cookies = request.form.get('cookies', '')
        token = extract_token(cookies)
        if token:
            result = token
        else:
            error = "Failed to extract token. Please check your cookies."
    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
