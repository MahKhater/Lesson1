import os
import random
from flask import Flask, render_template_string, request
from pypdf import PdfReader

app = Flask(__name__)

def extract_real_content_from_pdf():
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
            
    content_lines = []
    if pdf_path:
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    for line in text.split('\n'):
                        clean = line.strip()
                        # تصفية الأسطر لتكون جملاً مفيدة من محتوى الدرس
                        if len(clean) > 15 and not clean.startswith("http") and not clean.isdigit():
                            content_lines.append(clean)
        except Exception:
            pass
            
    return content_lines

@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 4))
    
    # استخراج النصوص الحقيقية من ملف lesson1.pdf
    pdf_sentences = extract_real_content_from_pdf()
    
    question_pool = []
    
    if pdf_sentences:
        # لو الكود قدر يقرا كلام حقيقي من الـ PDF، نحوله لأسئلة ذكية من صلب المحتوى
        for sentence in pdf_sentences:
            question_pool.append({
                "prompt": f"بناءً على ما ورد في درسك، اشرح أو وضح العبارة التالية: « {sentence} »",
                "hint": "الإجابة مستخرجة مباشرة من فقرات ملف (lesson1.pdf)."
            })
    
    # لو الملف مصور أو لسه محتاج دعم إضافي، ندمج محتوى تعليمي دقيق ومباشر للدرس
    if len(question_pool) < num_questions:
        fallback_lessons = [
            {"prompt": "ما هي الأركان أو الأساسيات التي تم شرحها في الجزء الأول من ملف الدرس؟", "hint": "راجع الترتيب التسلسلي للأفكار في ملف lesson1.pdf."},
            {"prompt": "وضح المقصود بالمصطلحات العلمية أو العملية الرئيسية الواردة في نص الدرس.", "hint": "ركز على الكلمات المفتاحية في المستند."},
            {"prompt": "ما هي النتيجة المباشرة المترتبة على القاعدة الأساسية المشروحة في ملف lesson1؟", "hint": "تحقق من استنتاجات الفقرة الرئيسية."},
            {"prompt": "كيف تتعامل مع الفكرة المركزية للدرس وتطبقها عملياً؟", "hint": "اربط الأمثلة الموجودة في الدرس بالتطبيق."},
            {"prompt": "استخرج من الدرس الأسباب التي تؤدي إلى النجاح في الفهم والتطبيق.", "hint": "راجع تفاصيل الشرح في الملف."},
            {"prompt": "ما هي الملاحظات الهامة التي يجب مراعاتها عند دراسة هذا الموضوع؟", "hint": "دقق في التنبيهات والنقاط البارزة بالدرس."}
        ]
        for item in fallback_lessons:
            if item not in question_pool:
                question_pool.append(item)

    # اختيار عدد الأسئلة حسب اختيار الطالب
    selected_pool = random.sample(question_pool, min(num_questions, len(question_pool)))
    
    questions = []
    for i, q in enumerate(selected_pool, 1):
        hint_style = f"مستوى ({level}) - " + q["hint"]
        questions.append({
            "id": i,
            "prompt": q["prompt"],
            "hint": hint_style
        })

    show_quiz = request.method == 'POST'
    
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>منصة سر التفوق - محتوى الدرس</title>
        <style>
            body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
            .main-card { max-width: 550px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
            .header-badge { text-align: center; color: #d4a373; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
            h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
            .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
            
            .section-title { font-weight: bold; color: #222; font-size: 15px; margin-bottom: 10px; }
            
            /* مستويات الصعوبة */
            .levels-container { display: flex; gap: 10px; margin-bottom: 20px; }
            .level-btn { flex: 1; padding: 12px; border: 2px solid #e0e0e0; border-radius: 12px; background: #fff; cursor: pointer; text-align: center; font-weight: bold; font-size: 14px; transition: 0.3s; }
            .level-btn input { display: none; }
            .level-btn.active, .level-btn:hover { border-color: #114b3e; background: #e8f5e9; color: #114b3e; }
            
            /* السلايدر */
            .slider-container { margin-bottom: 25px; background: #f9f9f9; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
            .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: bold; color: #114b3e; }
            input[type=range] { width: 100%; accent-color: #114b3e; cursor: pointer; }
            
            /* زر البدء */
            .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; }
            .start-btn:hover { background: #0d382f; }
            
            /* صندوق الأسئلة بعد البدء */
            .question-box { background: #fdfdfd; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px; border-right: 5px solid #114b3e; }
            .hint { color: #555; font-size: 13px; margin-top: 8px; background: #f1f8f6; padding: 8px; border-radius: 6px; }
            
            .lesson-badge { background: #f1f8f6; border: 1px solid #c8e6c9; padding: 12px; border-radius: 12px; text-align: center; margin-top: 20px; font-weight: bold; color: #114b3e; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="main-card">
            {% if not show_quiz %}
                <div class="header-badge">جاهز للتحدي؟ ✨</div>
                <h2>صمّم امتحانك</h2>
                <div class="subtitle">الدرس الأول: محتوى ملف lesson1.pdf</div>
                
                <form method="POST">
                    <div class="section-title">اختيار مستوى الصعوبة</div>
                    <div class="levels-container">
                        <label class="level-btn {% if level == 'مبتدئ' %}active{% endif %}">
                            <input type="radio" name="level" value="مبتدئ" {% if level == 'مبتدئ' %}checked{% endif %} onchange="updateActive(this)"> مبتدئ
                        </label>
                        <label class="level-btn {% if level == 'متوسط' %}active{% endif %}">
                            <input type="radio" name="level" value="متوسط" {% if level == 'متوسط' %}checked{% endif %} onchange="updateActive(this)"> متوسط
                        </label>
                        <label class="level-btn {% if level == 'محترف' %}active{% endif %}">
                            <input type="radio" name="level" value="محترف" {% if level == 'محترف' %}checked{% endif %} onchange="updateActive(this)"> محترف
                        </label>
                    </div>
                    
                    <div class="slider-container">
                        <div class="slider-header">
                            <span>عدد الأسئلة</span>
                            <span id="range-val" style="background: #114b3e; color: white; padding: 2px 10px; border-radius: 20px; font-size: 13px;">{{ num_questions }} أسئلة</span>
                        </div>
                        <input type="range" name="num_questions" min="1" max="10" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
                    </div>
                    
                    <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
                </form>
                
                <div class="lesson-badge">
                    📄 الأسئلة مستخرجة من محتوى: lesson1.pdf
                </div>
            {% else %}
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
                    <span style="font-size: 14px; color: #555;">المستوى: <strong>{{ level }}</strong></span>
                    <span style="font-size: 14px; color: #555;">عدد الأسئلة: <strong>{{ num_questions }}</strong></span>
                </div>
                
                <h2>بنك أسئلة الدرس الأول</h2>
                
                <div style="margin-top: 20px;">
                    {% for q in questions %}
                        <div class="question-box">
                            <p><strong>سؤال {{ q.id }}:</strong> {{ q.prompt }}</p>
                            <div class="hint">💡 <em>إرشاد:</em> {{ q.hint }}</div>
                        </div>
                    {% endfor %}
                </div>
                
                <a href="/" class="start-btn" style="text-align: center; margin-top: 20px;">🔄 تصميم امتحان جديد</a>
                <a href="https://wa.me/201221581154?s=t" class="start-btn" style="background: #25d366; text-align: center; margin-top: 10px;" target="_blank">تواصل عبر الواتساب للاشتراك 💬</a>
            {% endif %}
        </div>

        <script>
            function updateActive(radio) {
                document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
                radio.closest('.level-btn').classList.add('active');
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(HTML_TEMPLATE, level=level, num_questions=num_questions, questions=questions, show_quiz=show_quiz)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
