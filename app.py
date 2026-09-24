import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# بنك الأسئلة الشامل مقسم حسب مستويات الصعوبة مع الإجابة النموذجية الدقيقة
QUESTIONS_DB = {
    "مبتدئ": [
        {"id": 1, "type": "mcq", "prompt": "كلمة 'البيئة' مشتقة من الكلمة الفرنسية Environ والتي تعنى:", "options": ["المحيط", "الغلاف", "السطح", "النظام"], "answer": "المحيط", "hint": "تعني كل ما يحيط بنا."},
        {"id": 2, "type": "tf", "prompt": "تغطي المياه حوالي 70% من سطح كوكب الأرض.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "معلومة أساسية عن الغلاف المائي."},
        {"id": 3, "type": "mcq", "prompt": "النسبة الكبرى من المياه على سطح الأرض هي:", "options": ["مياه مالحة سائلة", "مياه عذبة سائلة", "مياه متجمدة", "مياه الأنهار"], "answer": "مياه مالحة سائلة", "hint": "تبلغ نسبتها حوالي 97%."},
        {"id": 4, "type": "tf", "prompt": "عملية النتح في النبات تنتج بخار ماء فقط.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "من خصائص عملية النتح في النبات."},
        {"id": 5, "type": "mcq", "prompt": "الفتحات الميكروسكوبية في أوراق النبات وتخرج منها الماء تسمى:", "options": ["الثغور", "النسيج", "الكلوروفيل", "الجذور"], "answer": "الثغور", "hint": "موجودة في أسطح الأوراق والسيقان الخضراء."}
    ],
    "متوسط": [
        {"id": 1, "type": "mcq", "prompt": "كل مما يلي يعتبر من العوامل اللاحيوية في النظام البيئي ما عدا:", "options": ["الضوء", "الهواء", "النباتات", "التربة"], "answer": "النباتات", "hint": "فكر في الفرق بين الكائنات الحية والعوامل غير الحية."},
        {"id": 2, "type": "tf", "prompt": "تعتبر النباتات والكائنات الدقيقة من العوامل اللاحيوية.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "النباتات كائنات حية وليست لاحيوية."},
        {"id": 3, "type": "mcq", "prompt": "تسمى الحركة المستمرة للماء حول الكرة الأرضية في مسارات مغلقة بـ:", "options": ["الدورة الهيدرولوجية", "عملية التمثيل الضوئي", "التحت الحيوي", "التوازن الصخري"], "answer": "الدورة الهيدرولوجية", "hint": "تعرف أيضاً بدورة الماء في الطبيعة."},
        {"id": 4, "type": "tf", "prompt": "المياه العذبة السائلة على كوكب الأرض تمثل نسبة 97%.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "97% هي نسبة المياه المالحة وليس العذبة."},
        {"id": 5, "type": "mcq", "prompt": "أي من عمليات دورة الماء تساهم بشكل مباشر في تكوين السحب؟", "options": ["التبخر", "التكثف", "التسرب", "الانصهار"], "answer": "التكثف", "hint": "تحول الحالة من غازية إلى سائلة معلقة."}
    ],
    "محترف": [
        {"id": 1, "type": "mcq", "prompt": "كيف تعد عملية التمثيل الضوئي دليلاً على التفاعل بين العوامل الحيوية واللاحيوية؟", "options": ["امتصاص ثاني أكسيد الكربون والضوء لإنتاج الجلوكوز", "فقدان الماء عبر الثغور لخفض الحرارة", "ذوبان الأملاح في الصخور لتكوين التربة", "حركة المياه الجوفية عبر مسام التربة"], "answer": "امتصاص ثاني أكسيد الكربون والضوء لإنتاج الجلوكوز", "hint": "تتطلب فهماً عميقاً لآلية البناء الضوئي."},
        {"id": 2, "type": "tf", "prompt": "تؤثر دورة الماء في تغيير سطح الأرض فيزيائياً وكيميائياً وبيولوجياً.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "راجع التأثيرات المختلفة لدورة الماء."},
        {"id": 3, "type": "mcq", "prompt": "ما هو الأثر الرئيسي لعملية النتح على النبات بجانب التخلص من الماء الزائد؟", "options": ["خفض درجة حرارة النبات وخلق قوة سحب للمياه", "إنتاج فضلات نيتروجينية كاليوريا", "تكوين السحب في الغلاف الجوي", "إذابة المعادن في الصخور المحيطة"], "answer": "خفض درجة حرارة النبات وخلق قوة سحب للمياه", "hint": "اربط بين خفض الحرارة وسحب الماء عبر نسيج الخشب."},
        {"id": 4, "type": "tf", "prompt": "الماء المتجمد في القمم والأنهار الجليدية يشكل حوالي 2% من مياه الأرض.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "تأكد من نسب توزيع المياه المتجمدة."},
        {"id": 5, "type": "mcq", "prompt": "أي العمليات التالية تعتبر مسؤولة عن تكوين المياه الجوفية في باطن الأرض؟", "options": ["تسرب المياه عبر مسام التربة والصخور الرسوبية", "تكثف بخار الماء لتكوين السحب", "النتح والتنفس في الكائنات الحية", "التبخر من المسطحات المائية الكبرى"], "answer": "تسرب المياه عبر مسام التربة والصخور الرسوبية", "hint": "تتم عبر حركة ورشح المياه خلال طبقات الأرض."}
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 3))
    action = request.form.get('action', 'select')
    
    pool = QUESTIONS_DB.get(level, QUESTIONS_DB["متوسط"])
    
    if request.method == 'GET' or action == 'select':
        return render_template_string(MAIN_TEMPLATE, level=level, num_questions=num_questions)
        
    elif action == 'generate':
        selected_questions = random.sample(pool, min(num_questions, len(pool)))
        return render_template_string(QUIZ_TEMPLATE, level=level, questions=selected_questions)
        
    elif action == 'grade':
        score = 0
        total = 0
        results = []
        
        # تصحيح دقيق لكل سؤال بناءً على الأسئلة المُرسلة
        for key in request.form:
            if key.startswith('q_'):
                q_idx = key.split('_')[1]
                user_ans = request.form.get(key)
                correct_ans = request.form.get(f'ans_{q_idx}')
                prompt = request.form.get(f'prompt_{q_idx}')
                
                total += 1
                is_correct = (user_ans == correct_ans)
                if is_correct:
                    score += 1
                    
                results.append({
                    "id": total,
                    "prompt": prompt,
                    "user_ans": user_ans if user_ans else "لم تتم الإجابة",
                    "correct_ans": correct_ans,
                    "is_correct": is_correct
                })
                
        return render_template_string(RESULT_TEMPLATE, level=level, score=score, total=total, results=results)

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - تصميم الامتحان</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .header-badge { text-align: center; color: #d4a373; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
        .section-title { font-weight: bold; color: #222; font-size: 15px; margin-bottom: 10px; }
        .levels-container { display: flex; gap: 10px; margin-bottom: 20px; }
        .level-btn { flex: 1; padding: 12px; border: 2px solid #e0e0e0; border-radius: 12px; background: #fff; cursor: pointer; text-align: center; font-weight: bold; font-size: 14px; transition: 0.3s; }
        .level-btn input { display: none; }
        .level-btn.active, .level-btn:hover { border-color: #114b3e; background: #e8f5e9; color: #114b3e; }
        .slider-container { margin-bottom: 25px; background: #f9f9f9; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
        .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: bold; color: #114b3e; }
        input[type=range] { width: 100%; accent-color: #114b3e; cursor: pointer; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .lesson-badge { background: #f1f8f6; border: 1px solid #c8e6c9; padding: 12px; border-radius: 12px; text-align: center; margin-top: 20px; font-weight: bold; color: #114b3e; font-size: 14px; }
    </style>
</head>
<body>
    <div class="main-card">
        <div class="header-badge">جاهز للتحدي؟ ✨</div>
        <h2>صمّم امتحانك</h2>
        <div class="subtitle">اختر مستواك وعدد الأسئلة للبدء فوراً</div>
        
        <form method="POST">
            <input type="hidden" name="action" value="generate">
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
                <input type="range" name="num_questions" min="1" max="5" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
            </div>
            
            <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
        </form>
        
        <div class="lesson-badge">📚 منصة سر التفوق الذكية للتعليم</div>
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

QUIZ_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - حل الاختبار</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .question-box { background: #fdfdfd; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 10px; border-right: 5px solid #114b3e; }
        .options-list { margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
        .option-item { background: #f9f9f9; border: 1px solid #e0e0e0; padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 14px; }
        .option-item:hover { background: #e8f5e9; border-color: #114b3e; }
        .option-item input { margin-left: 10px; }
        .badge-type { display: inline-block; background: #e8f5e9; color: #114b3e; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
        .hint { color: #555; font-size: 13px; margin-top: 10px; background: #f1f8f6; padding: 8px; border-radius: 6px; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
    </style>
</head>
<body>
    <div class="main-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
            <span style="font-size: 14px; color: #555;">المستوى: <strong style="color: #114b3e;">{{ level }}</strong></span>
        </div>
        <h2>اختبار الدرس الأول</h2>
        
        <form method="POST">
            <input type="hidden" name="action" value="grade">
            <input type="hidden" name="level" value="{{ level }}">
            
            <div style="margin-top: 20px;">
                {% for q in questions %}
                    <div class="question-box">
                        <span class="badge-type">{% if q.type == 'mcq' %}اختيار من متعدد{% else %}صح وخطأ{% endif %}</span>
                        <p><strong>سؤال {{ loop.index }}:</strong> {{ q.prompt }}</p>
                        
                        <input type="hidden" name="prompt_{{ loop.index }}" value="{{ q.prompt }}">
                        <input type="hidden" name="ans_{{ loop.index }}" value="{{ q.answer }}">
                        
                        <div class="options-list">
                            {% for opt in q.options %}
                                <label class="option-item">
                                    <!-- تم إزالة required لتجنب أي تعارض في المتصفح -->
                                    <input type="radio" name="q_{{ loop.index }}" value="{{ opt }}"> {{ opt }}
                                </label>
                            {% endfor %}
                        </div>
                        <div class="hint">💡 <em>{{ q.hint }}</em></div>
                    </div>
                {% endfor %}
            </div>
            
            <button type="submit" class="start-btn">تسليم الامتحان والتصحيح 📋</button>
        </form>
    </div>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نتيجة الامتحان - سر التفوق</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .score-box { background: #e8f5e9; border: 2px solid #2e7d32; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
        .score-num { font-size: 32px; font-weight: bold; color: #1b5e20; }
        .res-item { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px; }
        .correct { border-right: 5px solid #2e7d32; }
        .wrong { border-right: 5px solid #c62828; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .wa-btn { background: #25d366; margin-top: 10px; display: block; text-align: center; }
        .wa-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <h2>نتيجة اختبارك</h2>
        
        <div class="score-box">
            <p style="margin: 0 0 5px 0; font-size: 16px; color: #333;">لقد أتممت الاختبار بنجاح!</p>
            <div class="score-num">{{ score }} / {{ total }}</div>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #555;">المستوى: {{ level }}</p>
        </div>

        <h3>تفاصيل الإجابات:</h3>
        <div style="margin-top: 15px;">
            {% for r in results %}
                <div class="res-item {% if r.is_correct %}correct{% else %}wrong{% endif %}">
                    <p><strong>سؤال {{ r.id }}:</strong> {{ r.prompt }}</p>
                    <p style="margin: 5px 0; font-size: 14px;">إجابتك: <span style="font-weight: bold; color: {% if r.is_correct %}#2e7d32{% else %}#c62828{% endif %};">{{ r.user_ans }} {% if r.is_correct %}✅{% else %}❌{% endif %}</span></p>
                    {% if not r.is_correct %}
                        <p style="margin: 5px 0; font-size: 14px; color: #2e7d32;">الإجابة الصحيحة هي: <strong>{{ r.correct_ans }}</strong></p>
                    {% endif %}
                </div>
            {% endfor %}
        </div>

        <a href="/" class="start-btn" style="text-align: center; margin-top: 20px;">🔄 تصميم امتحان جديد</a>
        <a href="https://wa.me/201221581154?s=t" class="start-btn wa-btn" target="_blank">تواصل عبر الواتساب للاشتراك 💬</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
