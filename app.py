from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>منصة سر التفوق - تعمل بنجاح!</h1><br><a href='https://wa.me/201221581154?s=t'>تواصل عبر الواتساب للاشتراك</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
