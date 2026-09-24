import os
import random
from flask import Flask, render_template_string
from pypdf import PdfReader

app = Flask(__name__)

def generate_dynamic_questions():
    # قائمة بالأماكن المحتملة لوجود الملف لضمان قراءته بسلاسة
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
            
    questions = []
    
    try:
        if pdf_path:
            reader = PdfReader(pdf_path)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            # تقسيم النص إلى جمل أو أسطر مفيدة لتوليد الأسئلة
            lines = [line.strip() for line in full_text.split('\n') if len(line.strip()) > 15]
            
            if lines:
                # اختيار أسئلة متجددة عشوائياً من محتوى الـ PDF
                selected_lines = random.sample(lines, min(3, len(lines)))
                for i, line in enumerate(selected_lines, 1):
                    questions.append({
                        "id": i,
                        "prompt": f"بناءً على درسك، وضح المفهوم أو اشرح العبارة الآتية: '{line}'",
                        "hint": "الإجابة مستخرجة مباشرة من ملف الـ PDF الخاص بك."
                    })
            else:
                questions.append({"id": 1, "prompt": "ملف الـ PDF لا يحتوي على نصوص واضحة كفاية لتوليد الأسئلة.", "hint": "تأكد من محتوى الصفحات."})
        else:
            questions.append({"id": 1, "prompt": "عفواً، لم يتم العثور على ملف lesson1.pdf في أي مكان بالمشروع!", "hint": "تأكد من رفع الملف داخل مستودع جيت هب."})
    except Exception as e:
        questions.append({"id": 1, "prompt": f"حدث خطأ أثناء قراءة الملف: {e}", "hint": "خطأ تقني في المعالجة."})
        
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
        .btn { display: block; width: 100%; background: #007bff; color: white; padding: 12px; text-align: center; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; box-sizing: border-box; }
        .btn:hover { background: #0056b3; }
        .wa-btn { background: #25d366; margin-top: 10px; }
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

        <a href="/" class="btn">ابدأ مع سر التفوق 🚀</a>
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
