import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 4))
    
    # بنك الأسئلة المدمج (يشمل MCQ و True/False من محتوى الدرس الحقيقي)
    all_questions_pool = [
        {
            "type": "mcq",
            "prompt": "كلمة 'البيئة' مشتقة من الكلمة الفرنسية Environ والتي تعنى:",
            "options": ["المحيط", "الغلاف", "السطح", "النظام"],
            "hint": "تعني كل ما يحيط بنا."
        },
        {
            "type": "tf",
            "prompt": "تعتبر النباتات والكائنات الدقيقة من العوامل اللاحيوية في النظام البيئي.",
            "options": ["صح", "خطأ"],
            "hint": "النباتات كائنات حية إذن هي عوامل حيوية وليست لاحيوية."
        },
        {
            "type": "mcq",
            "prompt": "ما هي النسبة التي يغطيها الغلاف المائي من سطح كوكب الأرض تقريباً؟",
            "options": ["30%", "50%", "70%", "90%"],
            "hint": "بينما يشغل اليابس النسبة الباقية وهي 30%."
        },
        {
            "type": "tf",
            "prompt": "المياه العذبة السائلة على كوكب الأرض تمثل نسبة حوالي 97% من إجمالي المياه.",
            "options": ["صح", "خطأ"],
            "hint": "97% هي نسبة المياه المالحة السائلة، بينما العذبة السائلة 1%."
        },
        {
            "type": "mcq",
            "prompt": "تسمى الحركة المستمرة للماء من مكان لآخر حول الكرة الأرضية بـ:",
            "options": ["الدورة الهيدرولوجية", "عملية التمثيل الضوئي", "التحت الحيوي", "التوازن الصخري"],
            "hint": "وتعرف أيضاً بدورة الماء في الطبيعة."
        },
        {
            "type": "tf",
            "prompt": "عملية التكثف في دورة الماء هي المسؤول الرئيسي عن تكوين السحب في الغلاف الجوي.",
            "options": ["صح", "خطأ"],
            "hint": "التكثف يحول بخار الماء إلى قطرات مائية تكون السحب."
        },
        {
            "type": "mcq",
            "prompt": "عملية يتخلص فيها النبات من الماء الزائد على هيئة بخار ماء تسمى:",
            "options": ["الإخراج", "النتح", "التكثف", "الترسيب"],
            "hint": "تتم غالباً عبر الثغور في الأوراق والسيقان الخضراء."
        },
        {
            "type": "tf",
            "prompt": "عملية النتح في النبات تنتج بخار ماء فقط للمساعدة في خفض درجة حرارة النبات.",
            "options": ["صح", "خطأ"],
            "hint": "هذه هي التعريف العلمي الدقيق لعملية النتح."
        }
    ]
    
    # اختيار عدد الأسئلة عشوائياً بناءً على طلب الطالب
    selected_pool = random.sample(all_questions_pool, min(num_questions, len(all_questions_pool)))
    
    questions = []
    for i, q in enumerate(selected_pool, 1):
        questions.append({
            "id": i,
            "type": q["type"],
            "prompt": q["prompt"],
            "options": q["options"],
            "hint": f"مستوى ({level}) - إرشاد: {q['hint']}"
        })

    show_quiz = request.method == 'POST'
    
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>منصة سر التفوق - بنك الأسئلة الشامل</title>
        <style>
            body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
            .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
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
            .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
            .start-btn:hover { background: #0d382f; }
            
            /* صندوق الأسئلة */
            .question-box { background: #fdfdfd; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 10px; border-right: 5px solid #114b3e; }
            .options-list { margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
            .option-item { background: #f9f9f9; border: 1px solid #e0e0e0; padding: 10px 12px; border-radius: 8px; cursor: pointer; transition: 0.2s; font-size: 14px; }
            .option-item:hover { background: #e8f5e9; border-color: #114b3e; }
            .option-item input { margin-left: 10px; }
            
            .badge-type { display: inline-block; background: #e8f5e9; color: #114b3e; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
            .hint { color: #555; font-size: 13px; margin-top: 10px; background: #f1f8f6; padding: 8px; border-radius: 6px; }
            .lesson-badge { background: #f1f8f6; border: 1px solid #c8e6c9; padding: 12px; border-radius: 12px; text-align: center; margin-top: 20px; font-weight: bold; color: #114b3e; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="main-card">
            {% if not show_quiz %}
                <div class="header-badge">جاهز للتحدي؟ ✨</div>
                <h2>صمّم امتحانك</h2>
                <div class="subtitle">أسئلة (اختيار من متعدد + صح وخطأ) - الدرس الأول</div>
                
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
                        <input type="range" name="num_questions" min="1" max="8" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
                    </div>
                    
                    <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
                </form>
                
                <div class="lesson-badge">
                    📚 بنك الأسئلة الشامل للدرس الأول
                </div>
            {% else %}
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
                    <span style="font-size: 14px; color: #555;">المستوى: <strong>{{ level }}</strong></span>
                    <span style="font-size: 14px; color: #555;">عدد الأسئلة: <strong>{{ num_questions }}</strong></span>
                </div>
                
                <h2>اختبار الدرس الشامل</h2>
                
                <form method="GET" action="/">
                    <div style="margin-top: 20px;">
                        {% for q in questions %}
                            <div class="question-box">
                                <span class="badge-type">{% if q.type == 'mcq' %}اختيار من متعدد{% else %}صح وخطأ{% endif %}</span>
                                <p><strong>سؤال {{ q.id }}:</strong> {{ q.prompt }}</p>
                                <div class="options-list">
                                    {% for opt in q.options %}
                                        <label class="option-item">
                                            <input type="radio" name="q_{{ q.id }}" value="{{ opt }}"> {{ opt }}
                                        </label>
                                    {% endfor %}
                                </div>
                                <div class="hint">💡 <em>{{ q.hint }}</em></div>
                            </div>
                        {% endfor %}
                    </div>
                    
                    <button type="submit" class="start-btn" style="text-align: center; margin-top: 20px;">🔄 تصميم امتحان جديد</button>
                </form>
                
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
