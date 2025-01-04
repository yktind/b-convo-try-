from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Cookie to Access Token</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; }
        .container { max-width: 600px; margin: 50px auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        h2 { text-align: center; color: #333; }
        label { display: block; margin: 15px 0 5px; color: #555; }
        textarea, button { width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 5px; }
        button { background-color: #4CAF50; color: #fff; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .output { background: #e8f5e9; padding: 15px; border-radius: 5px; color: #2e7d32; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Convert Facebook Cookie to Access Token</h2>
        <form method="POST" action="/">
            <label for="cookie">Enter Facebook Cookie:</label>
            <textarea id="cookie" name="cookie" rows="5" placeholder="Paste your Facebook cookie here..." required></textarea>
            <button type="submit">Convert</button>
        </form>
        {% if token %}
        <div class="output">
            <strong>Access Token:</strong>
            <p>{{ token }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    token = None
    if request.method == 'POST':
        cookie = request.form['cookie'].strip()
        token = get_access_token(cookie)
    return render_template_string(HTML_TEMPLATE, token=token)

def get_access_token(cookie):
    """Converts Facebook cookie into an EAAB access token."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    cookies = {item.split('=')[0]: item.split('=')[1] for item in cookie.split('; ')}

    try:
        response = requests.get(
            "https://business.facebook.com/business_locations",
            headers=headers,
            cookies=cookies
        )
        if response.status_code == 200:
            # Extract EAAB token from the response
            token_match = re.search(r'EAAB\w+', response.text)
            if token_match:
                return token_match.group(0)
            else:
                return "Unable to extract access token. Check your cookie."
        else:
            return f"Error: Received status code {response.status_code} from Facebook."
    except requests.RequestException as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
