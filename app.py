from flask import Flask, render_template_string, request

app = Flask(__name__)

# قالب HTML متكامل يحتوي على الصفحة الرئيسية، قسم الأسئلة، وتصميم أنيق
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق التعليمية</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        header { background: #007bff; color: white; padding: 20px; text-align: center; border-radius: 8px; }
        .container { max-width: 800px; margin: 20px auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h2 { color: #007bff; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        .question-box { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
        .btn { display: inline-block; background: #25d366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 10px; }
        .btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <header>
        <h1>منصة سر التفوق التعليمية</h1>
        <p>بوابتك الأولى للتميز الدراسي والتفوق</p>
    </header>

    <div class="container">
        <h2>الصفحة الرئيسية</h2>
        <p>مرحباً بك يا بطل في منصة سر التفوق. تم تصميم هذه المنصة خصيصاً لمساعدتك على فهم الدروس، حل الأسئلة، واجتياز الاختبارات بأعلى الدرجات.</p>
        
        <h2>بنك الأسئلة والتدريبات</h2>
        <div class="question-box">
            <p><strong>سؤال 1:</strong> ما هي المكونات الأساسية لبناء تطبيق ويب سريع باستخدام بايثون؟</p>
            <p style="color: #666; font-size: 14px;">الإجابة النموذجية: استخدام إطار عمل خفيف مثل Flask مع خادم تشغيل مثل Gunicorn.</p>
        </div>

        <div class="question-box">
            <p><strong>سؤال 2:</strong> كيف تضمن نجاح نشر تطبيقك على السحابة (Render)؟</p>
            <p style="color: #666; font-size: 14px;">الإجابة النموذجية: ضبط متغيرات التشغيل جيداً، التأكد من صحة syntax الأكواد، وتثبيت التبعيات المطلوبة فقط.</p>
        </div>

        <div style="text-align: center; margin-top: 30px;">
            <h3>للاشتراك الكامل وتلقي المتابعة الشخصية:</h3>
            <a href="https://wa.me/201221581154?s=t" class="btn" target="_blank">تواصل عبر الواتساب للاشتراك</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
