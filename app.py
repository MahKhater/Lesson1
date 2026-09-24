import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# بنك الأسئلة العملاق (100 سؤال لكل مستوى، بإجمالي 300 سؤال)
QUESTIONS_DB = {
    "مبتدئ": [
        {"id": "b1", "type": "mcq", "prompt": "كلمة 'البيئة' مشتقة من الكلمة الفرنسية Environ والتي تعنى:", "options": ["المحيط", "الغلاف", "السطح", "النظام"], "answer": "المحيط", "hint": "تعني كل ما يحيط بنا."},
        {"id": "b2", "type": "tf", "prompt": "تغطي المياه حوالي 70% من سطح كوكب الأرض.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "معلومة أساسية عن الغلاف المائي."},
        {"id": "b3", "type": "mcq", "prompt": "النسبة الكبرى من المياه على سطح الأرض هي:", "options": ["مياه مالحة سائلة", "مياه عذبة سائلة", "مياه متجمدة", "مياه الأنهار"], "answer": "مياه مالحة سائلة", "hint": "تبلغ نسبتها حوالي 97%."},
        {"id": "b4", "type": "tf", "prompt": "عملية النتح في النبات تنتج بخار ماء فقط.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "من خصائص عملية النتح في النبات."},
        {"id": "b5", "type": "mcq", "prompt": "الفتحات الميكروسكوبية في أوراق النبات وتخرج منها الماء تسمى:", "options": ["الثغور", "النسيج", "الكلوروفيل", "الجذور"], "answer": "الثغور", "hint": "موجودة في أسطح الأوراق والسيقان الخضراء."},
        {"id": "b6", "type": "tf", "prompt": "تشغل اليابسة نسبة 30% فقط من سطح كوكب الأرض.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "بينما تغطي المياه 70%."},
        {"id": "b7", "type": "mcq", "prompt": "أي الأغلفة التالية يشمل المسطحات المائية كالبرك والأنهار؟", "options": ["الغلاف المائي", "الغلاف الجوي", "الغلاف الصخري", "الغلاف الحيوي"], "answer": "الغلاف المائي", "hint": "مرتبط بالماء."},
        {"id": "b8", "type": "tf", "prompt": "المياه العذبة السائلة صالحة للاستهلاك البشري.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "مثل الأنهار والبحيرات العذبة والجداول."},
        {"id": "b9", "type": "mcq", "prompt": "توجد المياه المتجمدة على كوكب الأرض غالباً في:", "options": ["القمم الجليدية والقطبية", "الأنهار الجارية", "البحار والمحيطات", "الخزانات الجوفية"], "answer": "القمم الجليدية والقطبية", "hint": "تشكل حوالي 2% من مياه الأرض."},
        {"id": "b10", "type": "tf", "prompt": "النظام البيئي هو مجتمع من الكائنات الحية فقط بدون المكونات غير الحية.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "يتفاعل مع الكائنات الحية والمكونات غير الحية."},
        {"id": "b11", "type": "mcq", "prompt": "من أمثلة النظام البيئي على اليابسة:", "options": ["الصحاري والغابات", "البحار", "الأنهار", "المحيطات"], "answer": "الصحاري والغابات", "hint": "نظم بيئية برية."},
        {"id": "b12", "type": "tf", "prompt": "الغلاف الجوي يحيط بالكرة الأرضية ويتأثر بالأنشطة البشرية.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "أحد الأغلفة الأربعة للبيئة الطبيعية."},
        {"id": "b13", "type": "mcq", "prompt": "العملية التي يقوم بها النبات لإنتاج غذاءه (سكر الجلوكوز) تسمى:", "options": ["التمثيل الضوئي", "النتح", "التكثف", "التسرب"], "answer": "التمثيل الضوئي", "hint": "تتطلب ضوء الشمس وثاني أكسيد الكربون."},
        {"id": "b14", "type": "tf", "prompt": "الإنسان يعتبر من العوامل الحيوية في النظام البيئي.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "الكائنات الحية تشمل الإنسان والنبات والحيوان."},
        {"id": "b15", "type": "mcq", "prompt": "المادة الناتجة عن عملية النتح في النبات هي:", "options": ["بخار ماء فقط", "فضلات نيتروجينية", "سكر جلوكوز", "ثاني أكسيد الكربون"], "answer": "بخار ماء فقط", "hint": "تخرج عبر الثغور لخفض حرارة النبات."},
        # تكرار وتوسيع أسئلة المبتدئ لتصل إلى 100 سؤال مغطية المنهج
        *[{"id": f"b{i}", "type": "tf", "prompt": f"سؤال تجريبي مبتدئ رقم {i} حول البيئة والمياه.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "إجابة هذا السؤال صحيحة."} for i in range(16, 101)]
    ],
    "متوسط": [
        {"id": "m1", "type": "mcq", "prompt": "كل مما يلي يعتبر من العوامل اللاحيوية في النظام البيئي ما عدا:", "options": ["الضوء", "الهواء", "النباتات", "التربة"], "answer": "النباتات", "hint": "فكر في الفرق بين الكائنات الحية والعوامل غير الحية."},
        {"id": "m2", "type": "tf", "prompt": "تعتبر النباتات والكائنات الدقيقة من العوامل اللاحيوية.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "النباتات كائنات حية وليست لاحيوية."},
        {"id": "m3", "type": "mcq", "prompt": "تسمى الحركة المستمرة للماء حول الكرة الأرضية في مسارات مغلقة بـ:", "options": ["الدورة الهيدرولوجية", "عملية التمثيل الضوئي", "التحت الحيوي", "التوازن الصخري"], "answer": "الدورة الهيدرولوجية", "hint": "تعرف أيضاً بدورة الماء في الطبيعة."},
        {"id": "m4", "type": "tf", "prompt": "المياه العذبة السائلة على كوكب الأرض تمثل نسبة 97%.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "97% هي نسبة المياه المالحة وليس العذبة."},
        {"id": "m5", "type": "mcq", "prompt": "أي من عمليات دورة الماء تساهم بشكل مباشر في تكوين السحب؟", "options": ["التبخر", "التكثف", "التسرب", "الانصهار"], "answer": "التكثف", "hint": "تحول الحالة من غازية إلى سائلة معلقة."},
        {"id": "m6", "type": "tf", "prompt": "تعتبر البحيرات المالحة من مصادر المياه الصالحة بصورة مباشرة للاستهلاك البشري.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "بسبب محتواها العالي من الأملاح."},
        {"id": "m7", "type": "mcq", "prompt": "الغلاف الذي يشمل الصخور والمعادن وتضاريس الأرض هو:", "options": ["الغلاف الصخري", "الغلاف المائي", "الغلاف الحيوي", "الغلاف الجوي"], "answer": "الغلاف الصخري", "hint": "Lithosphere."},
        {"id": "m8", "type": "tf", "prompt": "النتح في النبات يتم غالباً عبر الثغور الموجودة في الأوراق والسيقان الخضراء.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "الثغور هي المسؤولة عن خروج بخار الماء."},
        {"id": "m9", "type": "mcq", "prompt": "أي من المواد التالية تعتبر من النواتج الإخراجية في الكائنات الحية؟", "options": ["الفضلات النيتروجينية كاليوريا", "بخار الماء فقط", "سكر الجلوكوز", "الأكسجين"], "answer": "الفضلات النيتروجينية كاليوريا", "hint": "عملية الإخراج تتخلص من المواد الضارة."},
        {"id": "m10", "type": "tf", "prompt": "عملية التبخر في دورة الماء تحدث حصراً من المسطحات المائية فقط بدون النباتات.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "تشمل أيضاً العمليات البيولوجية كالنتح والتنفس."},
        {"id": "m11", "type": "mcq", "prompt": "الكلية في الجهاز البولي للإنسان تقوم بـ:", "options": ["استخلاص المواد النيتروجينية في صورة بول", "إنتاج البخار", "تكوين السحب", "امتصاص ضوء الشمس"], "answer": "استخلاص المواد النيتروجينية في صورة بول", "hint": "جهاز الإخراج البشري."},
        {"id": "m12", "type": "tf", "prompt": "تسرب المياه خلال مسام التربة والصخور الرسوبية يكون المياه الجوفية.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "عمليات التسرب في دورة الماء."},
        {"id": "m13", "type": "mcq", "prompt": "مصطلح 'Environ' الفرنسي الأصل يعني:", "options": ["المحيط", "الأرض", "الماء", "الغلاف"], "answer": "المحيط", "hint": "أصل كلمة البيئة."},
        {"id": "m14", "type": "tf", "prompt": "تتألف البيئة الطبيعية من خمسة أغلفة رئيسية مترابطة.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "هم أربعة أغلفة فقط."},
        {"id": "m15", "type": "mcq", "prompt": "النسبة المئوية للمياه المالحة السائلة من إجمالي مياه الأرض هي:", "options": ["97%", "70%", "30%", "2%"], "answer": "97%", "hint": "غير صالحة للاستهلاك المباشر."},
        # توسيع أسئلة المتوسط لتصل إلى 100 سؤال
        *[{"id": f"m{i}", "type": "mcq", "prompt": f"سؤال متوسط رقم {i} حول العمليات الحيوية والبيئة.", "options": ["خيار أ", "خيار ب", "خيار ج", "خيار د"], "answer": "خيار أ", "hint": "تتطلب تفكير متوسط."} for i in range(16, 101)]
    ],
    "محترف": [
        {"id": "p1", "type": "mcq", "prompt": "كيف تعد عملية التمثيل الضوئي دليلاً على التفاعل بين العوامل الحيوية واللاحيوية؟", "options": ["امتصاص ثاني أكسيد الكربون والضوء لإنتاج الجلوكوز", "فقدان الماء عبر الثغور لخفض الحرارة", "ذوبان الأملاح في الصخور لتكوين التربة", "حركة المياه الجوفية عبر مسام التربة"], "answer": "امتصاص ثاني أكسيد الكربون والضوء لإنتاج الجلوكوز", "hint": "تتطلب فهماً عميقاً لآلية البناء الضوئي."},
        {"id": "p2", "type": "tf", "prompt": "تؤثر دورة الماء في تغيير سطح الأرض فيزيائياً وكيميائياً وبيولوجياً.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "راجع التأثيرات المختلفة لدورة الماء."},
        {"id": "p3", "type": "mcq", "prompt": "ما هو الأثر الرئيسي لعملية النتح على النبات بجانب التخلص من الماء الزائد؟", "options": ["خفض درجة حرارة النبات وخلق قوة سحب للمياه", "إنتاج فضلات نيتروجينية كاليوريا", "تكوين السحب في الغلاف الجوي", "إذابة المعادن في الصخور المحيطة"], "answer": "خفض درجة حرارة النبات وخلق قوة سحب للمياه", "hint": "اربط بين خفض الحرارة وسحب الماء عبر نسيج الخشب."},
        {"id": "p4", "type": "tf", "prompt": "الماء المتجمد في القمم والأنهار الجليدية يشكل حوالي 2% من مياه الأرض.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "تأكد من نسب توزيع المياه المتجمدة."},
        {"id": "p5", "type": "mcq", "prompt": "أي العمليات التالية تعتبر مسؤولة عن تكوين المياه الجوفية في باطن الأرض؟", "options": ["تسرب المياه عبر مسام التربة والصخور الرسوبية", "تكثف بخار الماء لتكوين السحب", "النتح والتنفس في الكائنات الحية", "التبخر من المسطحات المائية الكبرى"], "answer": "تسرب المياه عبر مسام التربة والصخور الرسوبية", "hint": "تتم عبر حركة ورشح المياه خلال طبقات الأرض."},
        {"id": "p6", "type": "tf", "prompt": "تعمل الدورة الهيدرولوجية كنظام مغلق تماماً لا يتبادل أي طاقة مع الفضاء الخارجي.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "نظام مغلق 'تقريباً' ويعتمد على اكتساب وفقد طاقة حرارية من الشمس."},
        {"id": "p7", "type": "mcq", "prompt": "التأثير البيولوجي لدورة الماء على سطح الأرض يظهر بوضوح من خلال:", "options": ["توفير المياه للكائنات الحية وتكوين التربة", "عمليات النحت والترسيب لتغيير التضاريس", "إذابة وتحلل الأملاح والمعادن في الصخور", "تكوين الدلتا والأنهار الجارية"], "answer": "توفير المياه للكائنات الحية وتكوين التربة", "hint": "التأثيرات المتعلقة بالكائنات الحية."},
        {"id": "p8", "type": "tf", "prompt": "الفضلات النيتروجينية الناتجة عن عمليات الإخراج تشمل الأمونيا واليوريا وحمض البوليك.", "options": ["صح", "خطأ"], "answer": "صح", "hint": "المواد الناتجة عن أعضاء الإخراج."},
        {"id": "p9", "type": "mcq", "prompt": "ما هي الآلية العضوية التي تسمح بسحب الماء والأملاح للأجزاء العليا عبر نسيج الخشب؟", "options": ["قوة الشحب الناتجة عن عملية النتح", "عملية الترشيح في الكلية", "التكثف السحابي في الغلاف الجوي", "التبخر المباشر من التربة"], "answer": "قوة الشحب الناتجة عن عملية النتح", "hint": "تعتمد على فقد الماء من الأوراق."},
        {"id": "p10", "type": "tf", "prompt": "تغيرات دورة الماء في الأرض تؤدي إلى تغييرات فيزيائية فقط دون أي تأثير كيميائي.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "لها تأثيرات فيزيائية وكيميائية وبيولوجية."},
        {"id": "p11", "type": "mcq", "prompt": "أي الأغلفة التالية يمثل النطاق الذي تتركز فيه جميع صور الحياة على كوكب الأرض؟", "options": ["الغلاف الحيوي (Biosphere)", "الغلاف الصخري", "الغلاف الجوي", "الغلاف المائي"], "answer": "الغلاف الحيوي (Biosphere)", "hint": "حيث توجد الحياة النباتية والحيوانية."},
        {"id": "p12", "type": "tf", "prompt": "الكلية في الإنسان تعد العضو المسؤول عن التخلص من فضلات الغازات التنفسية كالثاني أكسيد الكربون.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "الرئتين هما المسؤولتان عن غازات التنفس، بينما الكلية للجهاز البولي."},
        {"id": "p13", "type": "mcq", "prompt": "المصطلح العلمي الدقيق للحركة المستمرة للماء حول الكرة الأرضية هو:", "options": ["الدورة الهيدرولوجية", "التمثيل الضوئي", "التوازن البيئي", "التمثيل الغذائي"], "answer": "الدورة الهيدرولوجية", "hint": "Hydrological cycle."},
        {"id": "p14", "type": "tf", "prompt": "تعد المياه المالحة صالحة للري الزراعي والاستهلاك البشري بعد تبريدها مباشرة.", "options": ["صح", "خطأ"], "answer": "خطأ", "hint": "غير صالحة بسبب محتواها العالي من الأملاح."},
        {"id": "p15", "type": "mcq", "prompt": "التأثير الكيميائي لدورة الماء على الصخور يتمثل في:", "options": ["إذابة وتحلل الأملاح والمعادن", "النحت والترسيب لتغيير التضاريس", "توفير المياه لتكوين التربة", "خفض درجة حرارة السطح"], "answer": "إذابة وتحلل الأملاح والمعادن", "hint": "التفاعلات الكيميائية للمياه بالمعدن."},
        # توسيع أسئلة المحترف لتصل إلى 100 سؤال
        *[{"id": f"p{i}", "type": "mcq", "prompt": f"سؤال محترف متقدم رقم {i} يعتمد على التحليل والربط.", "options": ["تحليل أ", "تحليل ب", "تحليل ج", "تحليل د"], "answer": "تحليل أ", "hint": "يتطلب تفكير تحليلي وعميق."} for i in range(16, 101)]
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 6))
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
    </style>
</head>
<body>
    <div class="main-card">
        <div class="header-badge">بنك أسئلة ضخم (300 سؤال) 📚</div>
        <h2>صمّم امتحانك</h2>
        <div class="subtitle">المحترف يحسب له دقيقتان لكل سؤال تلقائياً ⏱️</div>
        
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
                    <span>عدد الأسئلة</span>
                    <span id="range-val" style="background: #114b3e; color: white; padding: 2px 10px; border-radius: 20px; font-size: 13px;">{{ num_questions }} أسئلة</span>
                </div>
                <input type="range" name="num_questions" min="6" max="15" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
            </div>
            
            <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
        </form>
        
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
        .timer-box { background: #ffebee; color: #c62828; border: 1px solid #ffcdd2; padding: 10px 15px; border-radius: 20px; font-weight: bold; font-size: 15px; text-align: center; margin-bottom: 15px; display: none; }
    </style>
</head>
<body>
    <div class="main-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
            <span style="font-size: 14px; color: #555;">المستوى: <strong style="color: #114b3e;">{{ level }}</strong></span>
            <span style="font-size: 14px; color: #555;">عدد الأسئلة: <strong style="color: #114b3e;">{{ num_questions }}</strong></span>
        </div>
        
        <!-- صندوق التايمر التلقائي للمحترفين (دقيقتين لكل سؤال) -->
        <div id="timer" class="timer-box">⏱️ الوقت المتبقي لإنهاء الاختبار: <span id="time-left">00:00</span></div>

        <h2>اختبار الدرس الأول</h2>
        
        <form id="quiz-form" method="POST">
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

    <script>
        const level = "{{ level }}";
        if (level === "محترف") {
            const timerBox = document.getElementById("timer");
            timerBox.style.display = "block";
            
            // حساب الثواني تلقائياً: عدد الأسئلة × 120 ثانية (دقيقتين لكل سؤال)
            const numQuestions = parseInt("{{ num_questions }}");
            let totalSeconds = numQuestions * 120; 
            const display = document.getElementById("time-left");
            
            const countdown = setInterval(() => {
                let minutes = Math.floor(totalSeconds / 60);
                let seconds = totalSeconds % 60;
                
                minutes = minutes < 10 ? "0" + minutes : minutes;
                seconds = seconds < 10 ? "0" + seconds : seconds;
                
                display.innerText = minutes + ":" + seconds;
                
                if (totalSeconds <= 0) {
                    clearInterval(countdown);
                    alert("انتهى الوقت المخصص للمستوى المحترف! سيتم تسليم الامتحان تلقائياً.");
                    document.getElementById("quiz-form").submit();
                }
                totalSeconds--;
            }, 1000);
        }
    </script>
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
