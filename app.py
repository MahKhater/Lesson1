import os
import random
from flask import Flask, render_template_string, request
from pypdf import PdfReader

app = Flask(__name__)

def get_pdf_text():
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
            
    extracted_lines = []
    if pdf_path:
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    for line in text.split('\n'):
                        clean_line = line.strip()
                        if len(clean_line) > 10:
                            extracted_lines.append(clean_line)
        except Exception:
            pass
            
    return extracted_lines

@app.route('/', methods=['GET', 'POST'])
def index():
    # استلام خيارات الطالب من الديزاين
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 5))
    
    # محاولة سحب الكلام من lesson1.pdf
    pdf_lines = get_pdf_text()
    
    # بنك الأسئلة المستند لملف lesson1.pdf ومستويات الصعوبة
    base_questions = []
    if pdf_lines:
        for line in pdf_lines:
            base_questions.append({
                "prompt": f"بناءً على ما ورد في ملف (lesson1.pdf)، وضح المقصود أو اشرح: '{line}'",
                "hint": f"مستوى الصعوبة: {level} - مستخرج مباشرة من الدرس."
            })
    
    # لو الـ PDF صور وماجيبش سطور كفاية، نحط أسئلة احترافية مرتبطة بملف lesson1
    fallback_pool = [
        {"prompt": "ما هي الفكرة الأساسية والمحورية التي ناقشها ملف (lesson1.pdf)؟", "hint": f"المستوى ({level}): راجع الصفحة الأولى من الدرس."},
        {"prompt": "استخرج أهم العناصر أو النقاط الرئيسية المذكورة في درسك الأول.", "hint": f"المستوى ({level}): دقق في تفاصيل الملف."},
        {"prompt": "كيف يطبق المفهوم الرئيسي لملف (lesson1.pdf) في الواقع العملي؟", "hint": f"المستوى ({level}): ربط الفهم بالتطبيق."},
        {"prompt": "ما هي النتائج أو الأهداف التي يهدف درس (lesson1.pdf) لتحقيقها؟", "hint": f"المستوى ({level}): خلاصة الدرس."},
        {"prompt": "اشرح بإيجاز القاعدة المركزية التي بني عليها محتوى (lesson1.pdf).", "hint": f"المستوى ({level}): التفكير النقدي."}
    ]
    
    pool = base_questions if len(base_questions) >= num_questions else (base_questions + fallback_pool)
    
    # اختيار عدد الأسئلة اللي اختارها الطالب
    selected_questions = random.sample(pool, min(num_questions, len(pool))) if pool else fallback_pool[:num_questions]
    
    generated_questions = []
    for i, q in enumerate(selected_questions, 1):
        generated_questions.append({
            "id": i,
            "prompt": q["prompt"],
            "hint": q["hint"]
        })

    # لو لسه مفيش ضغط على زرار البدء، نعرض واجهة الاختيار (الديزاين الجديد)
    show_quiz = request.method == 'POST'
    
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>منصة سر التفوق - تحدي lesson1.pdf</title>
        <style>
            body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
            .main-card { max-width: 500px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
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
            .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; }
            .start-btn:hover { background: #0d382f; }
            
            .footer-info { text-align: center; font-size: 12px; color: #888; margin-top: 15px; }
            
            /* صندوق الأسئلة بعد البدء */
            .question-box { background: #fdfdfd; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px; border-right: 5px solid #114b3e; }
            .hint { color: #666; font-size: 13px; margin-top: 5px; }
            .back-btn { display: block; text-align: center; background: #6c757d; color: white; padding: 10px; border-radius: 10px; text-decoration: none; margin-top: 15px; font-weight: bold; }
            
            .lesson-badge { background: #f1f8f6; border: 1px solid #c8e6c9; padding: 12px; border-radius: 12px; text-align: center; margin-top: 20px; font-weight: bold; color: #114b3e; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="main-card">
            {% if not show_quiz %}
                <div class="header-badge">جاهز للتحدي؟ ✨</div>
                <h2>صمّم امتحانك</h2>
                <div class="subtitle">الدرس الأول: مستخرج مباشرة من (lesson1.pdf)</div>
                
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
                    📄 الأسئلة من ملف: lesson1.pdf فقط
                </div>
            {% else %}
                <h2>بنك أسئلة الدرس الأول</h2>
                <div class="subtitle">المستوى: <strong>{{ level }}</strong> | عدد الأسئلة: <strong>{{ num_questions }}</strong></div>
                
                <div style="margin-top: 20px;">
                    {% for q in questions %}
                        <div class="question-box">
                            <p><strong>سؤال {{ q.id }}:</strong> {{ q.prompt }}</p>
                            <p class="hint">💡 <em>توجيه:</em> {{ q.hint }}</p>
                        </div>
                    {% endfor %}
                </div>
                
                <a href="/" class="start-btn" style="text-decoration: none; text-align: center; margin-top: 20px; display: block;">🔄 تصميم امتحان جديد</a>
                <a href="https://wa.me/201221581154?s=t" class="back-btn" style="background: #25d366;" target="_blank">تواصل عبر الواتساب للاشتراك</a>
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
    return render_template_string(HTML_TEMPLATE, level=level, num_questions=num_questions, questions=generated_questions, show_quiz=show_quiz)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
