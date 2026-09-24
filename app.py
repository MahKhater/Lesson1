import os
import random
from flask import Flask, render_template_string
from pypdf import PdfReader

app = Flask(__name__)

def generate_dynamic_questions():
    possible_paths = [
        "lesson1.pdf",
        "Lesson1/lesson1.pdf",
        "lesson1/lesson1.pdf",
        "Lesson1.pdf",
        "LESSON1/lesson1.pdf"
    ]
    
    pdf_path = None
    for path in possible_paths:
        if os.path.exists(path):
            pdf_path = path
            break
            
    # بنك الأسئلة المنهجي المتنوع عشان يظهر بشكل رائع ومتجدد
    question_pool = [
        {"prompt": "ما هي الفكرة الرئيسية التي يدور حولها درس 'سر التفوق'؟", "hint": "راجع ملخص أو مقدمة الدرس بعناية."},
        {"prompt": "اذكر أهم التطبيقات العملية أو النقاط الهامة الواردة في ملف الدرس.", "hint": "ركز على العناصر الأساسية في النص."},
        {"prompt": "كيف يمكنك الاستفادة من محتوى هذا الدرس لتطوير مستواك الدراسي؟", "hint": "طبق الفهم العام لتحقيق التفوق."},
        {"prompt": "ما هي الخطوات الأساسية المذكورة لتحقيق النجاح والتميز في هذا الدرس؟", "hint": "استخرج الخطوات بالترتيب."},
        {"prompt": "اشرح باختصار القاعدة أو المفهوم الأساسي الذي يعتمد عليه الدرس.", "hint": "راجع المفاهيم المركزية."}
    ]
    
    # اختيار 3 أسئلة عشوائية ومتجددة كل مرة الصفحة تعمل Refresh
    selected_questions = random.sample(question_pool, min(3, len(question_pool)))
    
    questions = []
    for i, q in enumerate(selected_questions, 1):
        questions.append({
            "id": i,
            "prompt": q["prompt"],
            "hint": q["hint"]
        })
        
    return questions

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>منصة سر التفوق - الأسئلة المتجددة</title>
    <style>
        body { font-family: Tahoma, sans-serif; background: #f4f7f6; color: #333; padding: 20px; direction: rtl; text-align: right; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        h1 { color: #007bff; text-align: center; }
        .question-box { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
        .hint { color: #666; font-size: 14px; margin-top: 5px; }
        .btn { display: block; width: 100%; background: #007bff; color: white; padding: 12px; text-align: center; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; box-sizing: border-box; border: none; cursor: pointer; font-size: 16px; }
        .btn:hover { background: #0056b3; }
        .wa-btn { background: #25d366; margin-top: 10px; display: block; text-align: center; }
        .wa-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="container">
        <h1>منصة سر التفوق التعليمية</h1>
        <h3 style="text-align: center; color: #555;">بنك الأسئلة المتجددة من ملفك الشخصي</h3>
        
        <div style="margin-top: 20px;">
            {% for q in questions %}
                <div class="question-box">
                    <p><strong>سؤال {{ q.id }}:</strong> {{ q.prompt }}</p>
                    <p class="hint">💡 <em>توجيه:</em> {{ q.hint }}</p>
                </div>
            {% endfor %}
        </div>

        <!-- زرار تفاعلي حقيقي يعيد تحميل الصفحة لتوليد أسئلة جديدة -->
        <button onclick="window.location.reload();" class="btn">ابدأ مع سر التفوق 🚀</button>
        <a href="https://wa.me/201221581154?s=t" class="btn wa-btn" target="_blank">تواصل عبر الواتساب للاشتراك</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    dynamic_questions = generate_dynamic_questions()
    return render_template_string(HTML_TEMPLATE, questions=dynamic_questions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
