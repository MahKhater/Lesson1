import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# بنك الأسئلة الحقيقي والموسع
QUESTIONS_DB = {
    "مبتدئ": [
        {"id": "b1", "type": "mcq", "prompt": "كلمة 'البيئة' مشتقة من الكلمة الفرنسية Environ والتي تعنى:", "options": ["المحيط", "الغلاف", "السطح", "النظام"], "answer": "المحيط", "hint": "تعني كل ما يحيط بالإنسان وكائنات حيّة."},
        {"id": "b2", "type": "tf", "prompt": "تغطي المياه حوالي 70% من سطح كوكب الأرض.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "النسبة الباقية لليابسة."},
        {"id": "b3", "type": "mcq", "prompt": "النسبة الكبرى من المياه على سطح الأرض تتمثل في:", "options": ["مياه مالحة سائلة", "مياه عذبة سائلة", "مياه متجمدة", "مياه الأنهار الجارية"], "answer": "مياه مالحة سائلة", "hint": "تبلغ نحو 97% من المياه."},
        {"id": "b4", "type": "tf", "prompt": "عملية النتح في النبات تنتج بخار ماء فقط.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "تخرج عبر الثغور النباتية."},
        {"id": "b5", "type": "mcq", "prompt": "الفتحات الميكروسكوبية الدقيقة في أوراق النباتات تسمى:", "options": ["الثغور", "النسيج", "الكلوروفيل", "الجذور"], "answer": "الثغور", "hint": "موجودة على أسطح الأوراق."},
        {"id": "b6", "type": "tf", "prompt": "تشغل اليابسة نسبة 30% تقريباً من إجمالي مساحة الأرض.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "تتوزع على القارات المختلفة."},
        {"id": "b7", "type": "mcq", "prompt": "أي الأغلفة التالية يشمل المسطحات المائية كالبرك والبحار والأنهار؟", "options": ["الغلاف المائي", "الغلاف الجوي", "الغلاف الصخري", "الغلاف الحيوي"], "answer": "الغلاف المائي", "hint": "متعلق بالمياه بكل أشكالها."},
        {"id": "b8", "type": "tf", "prompt": "المياه العذبة السائلة صالحة للاستهلاك البشري المباشر.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "مثل الأنهار والبحيرات العذبة."},
        {"id": "b9", "type": "mcq", "prompt": "توجد المياه المتجمدة على كوكب الأرض غالباً في:", "options": ["القمم الجليدية والقطبية", "الأنهار الجارية", "البحار والمحيطات", "الخزانات الجوفية"], "answer": "القمم الجليدية والقطبية", "hint": "تشكل نسبة الثلوج والجليد."},
        {"id": "b10", "type": "tf", "prompt": "النظام البيئي يقتصر على الكائنات الحية فقط ولا يضم مكونات غير حية.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "يجمع بين عناصر حية ولاحيوية."}
    ],
    "متوسط": [
        {"id": "m1", "type": "mcq", "prompt": "كل مما يلي يعتبر من العوامل اللاحيوية في النظام البيئي ما عدا:", "options": ["الضوء", "الهواء", "النباتات", "التربة"], "answer": "النباتات", "hint": "النبات كائن حي حيوي."},
        {"id": "m2", "type": "tf", "prompt": "تعتبر النباتات والكائنات الدقيقة من العوامل اللاحيوية.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "كائنات حية."},
        {"id": "m3", "type": "mcq", "prompt": "تسمى الحركة المستمرة للماء حول الكرة الأرضية في مسارات مغلقة بـ:", "options": ["الدورة الهيدرولوجية", "التمثيل الضوئي", "التوازن الصخري", "التحلل الحيوي"], "answer": "الدورة الهيدرولوجية", "hint": "دورة الماء الطبيعية."},
        {"id": "m4", "type": "tf", "prompt": "المياه العذبة السائلة على كوكب الأرض تمثل نسبة 97%.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "97% نسبة المياه المالحة."},
        {"id": "m5", "type": "mcq", "prompt": "أي من عمليات دورة الماء تساهم بشكل مباشر في تكوين السحب؟", "options": ["التبخر والتكثف", "التسرب الجوفي", "الحت والترسيب", "النتح الأرضي"], "answer": "التبخر والتكثف", "hint": "تبخر ثم تكثف بالجو."},
        {"id": "m6", "type": "tf", "prompt": "تعتبر البحيرات المالحة صالحة للاستهلاك البشري المباشر.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "تحتوي على أملاح عالية."},
        {"id": "m7", "type": "mcq", "prompt": "الغلاف الذي يشمل الصخور والمعادن وتضاريس الأرض هو:", "options": ["الغلاف الصخري", "الغلاف المائي", "الغلاف الحيوي", "الغلاف الجوي"], "answer": "الغلاف الصخري", "hint": "القشرة الأرضية."},
        {"id": "m8", "type": "tf", "prompt": "النتح في النبات يتم عبر الثغور الموجودة في الأوراق والسيقان الخضراء.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "فقد الماء بصورة بخار."},
        {"id": "m9", "type": "mcq", "prompt": "أي من المواد التالية تعتبر من النواتج الإخراجية في الكائنات الحية؟", "options": ["الفضلات النيتروجينية كاليوريا", "سكر الجلوكوز", "الأكسجين المنتج", "الكلوروفيل"], "answer": "الفضلات النيتروجينية كاليوريا", "hint": "تخرج عبر الجهاز البولي."},
        {"id": "m10", "type": "tf", "prompt": "عملية التبخر في دورة الماء تحدث من المسطحات المائية فقط وتلغي النباتات.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "تشمل النتح والتبخر النباتي والحيواني."}
    ],
    "محترف": [
        {"id": "p1", "type": "mcq", "prompt": "كيف تعد عملية التمثيل الضوئي دليلاً على التفاعل المباشر بين العوامل الحيوية واللاحيوية؟", "options": ["امتصاص ثاني أكسيد الكربون والضوء (لاحيوي) لإنتاج الجلوكوز بواسطة النبات (حيوي)", "فقدان الماء عبر الثغور لخفض درجة حرارة الأوراق", "ذوبان الأملاح والمعادن في الصخور لتكوين التربة الزراعية", "حركة المياه الجوفية عبر مسام التربة الرملية الرسوبية"], "answer": "امتصاص ثاني أكسيد الكربون والضوء (لاحيوي) لإنتاج الجلوكوز بواسطة النبات (حيوي)", "hint": "تفاعل عناصر حية مع غير حية."},
        {"id": "p2", "type": "tf", "prompt": "تؤثر دورة الماء في تغيير معالم سطح الأرض فيزيائياً وكيميائياً وبيولوجياً.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "دورات التعرية والترسيب والتحلل."},
        {"id": "p3", "type": "mcq", "prompt": "ما هو المقصود بالبصمة البيئية للإنسان أو المجتمع؟", "options": ["مقياس لمساحة الأرض والمياه اللازمة لإنتاج الموارد المستهلكة واستيعاب النفايات", "حجم الأثر الحراري للرياح على تضاريس القارات", "كمية الأمطار الساقطة على مساحة محددة سنوياً", "سرعة استنزاف الخزانات الجوفية العميقة"], "answer": "مقياس لمساحة الأرض والمياه اللازمة لإنتاج الموارد المستهلكة واستيعاب النفايات", "hint": "Ecological footprint."},
        {"id": "p4", "type": "mcq", "prompt": "أي من الآتي يمثل مؤشراً حيوياً دقيقاً على تلوث الهواء البيئي؟", "options": ["حساسية الأشنات Lichens واختفاؤها من المناطق الملوثة", "كثرة النباتات الخضراء المزهرة بالمدن الصناعية", "وفرة الأسماك النهرية الحساسة بالمجاري الملوثة", "نشاط الطيور المهاجرة وسط العوادم"], "answer": "حساسية الأشنات Lichens واختفاؤها من المناطق الملوثة", "hint": "مؤشرات بيولوجية للتلوث."},
        {"id": "p5", "type": "tf", "prompt": "تعتبر المياه الجوفية جزءاً أساسياً من الغلاف المائي.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "مياه باطن الأرض."},
        {"id": "p6", "type": "tf", "prompt": "تعمل الدورة الهيدرولوجية كنظام مغلق تماماً لا يتبادل طاقة مع الفضاء.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "نظام يعتمد على اكتساب وفقد طاقة حرارية شمسية."},
        {"id": "p7", "type": "mcq", "prompt": "ما هي النتيجة المباشرة لزيادة انبعاثات غازات الدفيئة بكثافة في الغلاف الجوي؟", "options": ["تعزيز ظاهرة الاحتباس الحراري وزيادة متوسط حرارة الأرض", "توسيع طبقة الأوزون وزيادة حمايتها للأشعة", "زيادة كمية المياه العذبة المتجمدة بالقطبين", "تنشيط معدلات التمثيل الضوئي السلبي"], "answer": "تعزيز ظاهرة الاحتباس الحراري وزيادة متوسط حرارة الأرض", "hint": "احتباس الحرارة الإشعاعية للأرض."},
        {"id": "p8", "type": "tf", "prompt": "الفضلات النيتروجينية الناتجة عن عمليات الإخراج الحيواني تشمل الأمونيا واليوريا وحمض البوليك.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "صور التخلص من الفضلات الأيضية."},
        {"id": "p9", "type": "mcq", "prompt": "أي من التكيفات التالية يعتبر تكيفاً سلوكياً يساعد الحيوانات على تجنب درجات الحرارة المرتفعة؟", "options": ["البيات الصيفي أو اللجوء للجحادات والجحور تحت الأرض", "تطور فرو سميك وعازل للحرارة", "امتلاك أذان طهو طويلة لتبديد الحرارة", "تغير لون الجلد ليتوافق مع البيئة المحيطة"], "answer": "البيات الصيفي أو اللجوء للجحادات والجحور تحت الأرض", "hint": "سلوك وليس تركيب جسمي."},
        {"id": "p10", "type": "tf", "prompt": "تتطلب الإدارة المستدامة للموارد المائية خفض الهدر والتلوث وتحسين كفاءة الاستخدام.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "الحفاظ على الموارد للأجيال."}
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 5))
    action = request.form.get('action', 'select')
    
    pool = QUESTIONS_DB.get(level, QUESTIONS_DB["متوسط"])
    
    if request.method == 'GET' or action == 'select':
        return render_template_string(MAIN_TEMPLATE, level=level, num_questions=num_questions)
        
    elif action == 'generate':
        selected_questions = random.sample(pool, min(num_questions, len(pool)))
        return render_template_string(QUIZ_TEMPLATE, level=level, num_questions=len(selected_questions), questions=selected_questions)
        
    elif action == 'grade':
        score = 0
        total = 0
        results = []
        
        for key in request.form:
            if key.startswith('q_'):
                qid = key.split('_')[1]
                user_ans = request.form.get(key)
                correct_ans = request.form.get(f'ans_{qid}')
                prompt = request.form.get(f'prompt_{qid}')
                
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
        .whatsapp-link-btn { display: block; width: 100%; background: #25d366; color: white; padding: 13px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 15px; text-decoration: none; box-shadow: 0 4px 10px rgba(37,211,102,0.3); transition: 0.3s; margin-top: 15px; box-sizing: border-box; }
        .whatsapp-link-btn:hover { background: #1ebe57; }
        .print-btn { background: #455a64; margin-top: 10px; }
        .print-btn:hover { background: #37474f; }
        @media print {
            body { background: white; padding: 0; }
            .whatsapp-link-btn, .print-btn, .start-btn { display: none !important; }
            .main-card { box-shadow: none; padding: 0; }
        }
    </style>
</head>
<body>
    <div class="main-card">
        <div class="header-badge">منصة سر التفوق التعليمية ✨</div>
        <h2>صمّم امتحانك</h2>
        <div class="subtitle">اختبر معلوماتك الآن بكل سهولة ⏱️</div>
        
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
                    <input type="radio" name="level" value="محترف" {% if level == 'محترف' %}checked{% endif %} onchange="updateActive(this)"> محترف ⏱️
                </label>
            </div>
            
            <div class="slider-container">
                <div class="slider-header">
                    <span>عدد الأسئلة بالاختبار</span>
                    <span id="range-val" style="background: #114b3e; color: white; padding: 2px 10px; border-radius: 20px; font-size: 13px;">{{ num_questions }} أسئلة</span>
                </div>
                <input type="range" name="num_questions" min="3" max="10" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
            </div>
            
            <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
        </form>
        
        <button type="button" class="start-btn print-btn" onclick="window.print()">🖨️ طباعة الصفحة الأولى</button>
        <a href="https://wa.me/201221581154?s=t" class="whatsapp-link-btn" target="_blank">💬 للاشتراك اضغط هنا</a>
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
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
            <span style="font-size: 14px; color: #555;">المستوى: <strong style="color: #114b3e;">{{ level }}</strong></span>
            <span style="font-size: 14px; color: #555;">عدد الأسئلة: <strong style="color: #114b3e;">{{ num_questions }}</strong></span>
        </div>

        <h2>اختبار الدرس الأول الشامل</h2>
        
        <form method="POST">
            <input type="hidden" name="action" value="grade">
            <input type="hidden" name="level" value="{{ level }}">
            
            <div style="margin-top: 20px;">
                {% for q in questions %}
                    <div class="question-box">
                        <span class="badge-type">{% if q.type == 'mcq' %}اختيار من متعدد{% else %}صح وخطأ{% endif %}</span>
                        <p><strong>سؤال {{ loop.index }}:</strong> {{ q.prompt }}</p>
                        
                        <input type="hidden" name="prompt_{{ q.id }}" value="{{ q.prompt }}">
                        <input type="hidden" name="ans_{{ q.id }}" value="{{ q.answer }}">
                        
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
        .print-btn { background: #455a64; margin-top: 10px; }
        .print-btn:hover { background: #37474f; }
        @media print {
            body { background: white; padding: 0; }
            .start-btn, .wa-btn, .print-btn { display: none !important; }
            .main-card { box-shadow: none; padding: 0; }
        }
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

        <button type="button" class="start-btn print-btn" onclick="window.print()">🖨️ طباعة النتيجة</button>
        <a href="/" class="start-btn" style="text-align: center; margin-top: 10px;">🔄 تصميم امتحان جديد</a>
        <a href="https://wa.me/201221581154?s=t" class="start-btn wa-btn" target="_blank">تواصل عبر الواتساب للاشتراك 💬</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
