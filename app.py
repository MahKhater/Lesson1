import os
from flask import Flask, render_template_string, request, jsonify
from pypdf import PdfReader
import google.generativeai as genai

app = Flask(_name_)

# إعداد مفتاح الذكاء الاصطناعي
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=API_KEY)

PDF_PATH = "lesson1.pdf"

def extract_pdf_text(pdf_path):
    if not os.path.exists(pdf_path):
        return "الأسئلة مش موجودة حاليا.. ابعت رسالة على الواتس 01221581154"
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text

@app.route('/')
def index():
    html_template = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>منصة سر التفوق التعليمية</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); margin: 0; padding: 20px; color: #333; min-height: 100vh; }
            .container { max-width: 850px; margin: 0 auto; background: white; padding: 35px; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.12); }
            .brand-header { text-align: center; margin-bottom: 25px; }
            .brand-badge { background: #2c3e50; color: #f1c40f; display: inline-block; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 14px; margin-bottom: 10px; letter-spacing: 1px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; margin: 5px 0; font-size: 28px; }
            .subtitle { color: #7f8c8d; font-size: 15px; margin-top: 5px; }
            .chat-box { height: 420px; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; overflow-y: scroll; background: #fafbfc; margin-bottom: 20px; display: flex; flex-direction: column; gap: 12px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); }
            .message { padding: 12px 18px; border-radius: 12px; max-width: 82%; line-height: 1.6; font-size: 15px; }
            .user-msg { background: #3498db; color: white; align-self: flex-start; border-bottom-left-radius: 2px; }
            .ai-msg { background: #edf2f7; color: #2d3748; align-self: flex-end; border-bottom-right-radius: 2px; border: 1px solid #e2e8f0; }
            .input-area { display: flex; gap: 12px; }
            input[type="text"] { flex: 1; padding: 14px; border: 1px solid #cbd5e1; border-radius: 10px; font-size: 16px; outline: none; transition: border-color 0.2s; }
            input[type="text"]:focus { border-color: #3498db; }
            button { background: #27ae60; color: white; border: none; padding: 14px 28px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.2s, transform 0.1s; }
            button:hover { background: #219653; }
            button:active { transform: scale(0.98); }
            .pdf-link-container { text-align: center; margin-bottom: 20px; background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px dashed #cbd5e1; }
            .pdf-link { color: #2980b9; text-decoration: none; font-weight: bold; font-size: 14px; }
            .pdf-link:hover { text-decoration: underline; }
            .footer { text-align: center; margin-top: 25px; font-size: 13px; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="brand-header">
                <div class="brand-badge">⚡ براند سر التفوق</div>
                <h1>منصة الشرح الذكي للثانوية العامة</h1>
                <div class="subtitle">استفسر عن أي نقطة في الدرس وسيجاوبك المعلم الذكي فوراً وبدون تسجيل دخول!</div>
            </div>
            
            <div class="pdf-link-container">
                <a href="/view-pdf" target="_blank" class="pdf-link">📄 استعرض ملف الدرس الأصلي (PDF) لمراجعته في أي وقت</a>
            </div>

            <div class="chat-box" id="chatBox">
                <div class="message ai-msg">أهلاً بك يا بطل في منصة <b>سر التفوق</b>! 🎓 أنا مساعدك الذكي جاهز لأي سؤال يخص محتوى درس اليوم، اسأل ولا تتردد!</div>
            </div>

            <div class="input-area">
                <input type="text" id="userInput" placeholder="اكتب سؤالك هنا بخصوص الدرس..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">إرسال</button>
            </div>
            
            <div class="footer">
                جميع الحقوق محفوظة © سر التفوق - إتاحة تعليمية متكاملة 24/7
            </div>
        </div>

        <script>
            function appendMessage(text, sender) {
                const chatBox = document.getElementById('chatBox');
                const msgDiv = document.createElement('div');
                msgDiv.className = message ${sender === 'user' ? 'user-msg' : 'ai-msg'};
                msgDiv.innerHTML = text.replace(/\\n/g, '<br>');
                chatBox.appendChild(msgDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            async function sendMessage() {
                const input = document.getElementById('userInput');
                const text = input.value.trim();
                if (!text) return;

                appendMessage(text, 'user');
                input.value = '';

                const loadingId = 'loading-' + Date.now();
                const chatBox = document.getElementById('chatBox');
                const loadDiv = document.createElement('div');
                loadDiv.className = 'message ai-msg';
                loadDiv.id = loadingId;
                loadDiv.innerHTML = '<i>جاري تحليل الدرس وصياغة الإجابة...</i>';
                chatBox.appendChild(loadDiv);
                chatBox.scrollTop = chatBox.scrollHeight;

                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ question: text })
                    });
                    const data = await response.json();
                    document.getElementById(loadingId).remove();
                    appendMessage(data.answer || 'عذراً، حدث خطأ في الرد.', 'ai');
                } catch (e) {
                    document.getElementById(loadingId).remove();
                    appendMessage('حدث خطأ في الاتصال بالخادم.', 'ai');
                }
            }

            function handleKeyPress(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'answer': 'الرجاء إدخال سؤال صحيح.'})

    pdf_text = extract_pdf_text(PDF_PATH)
    
    # إذا كان الملف فارغاً أو غير موجود
    if "الأسئلة مش موجودة" in pdf_text:
        return jsonify({'answer': pdf_text})

    prompt = f"""
    أنت مساعد تعليمي ذكي لمنصة "سر التفوق" التعليمية ومخصص لشرح محتوى الدروس للطلاب.
    بناءً على محتوى ملف الدرس التالي فقط، أجب عن سؤال الطالب بدقة ووضوح وبأسلوب تربوي محفز:
    
    محتوى الدرس:
    {pdf_text}
    
    سؤال الطالب: {question}
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        answer = response.text
    except Exception as e:
        answer = f"الأسئلة مش موجودة حاليا.. ابعت رسالة على الواتس 01221581154"

    return jsonify({'answer': answer})

@app.route('/view-pdf')
def view_pdf():
    from flask import send_file
    if os.path.exists(PDF_PATH):
        return send_file(PDF_PATH)
    return "الملف غير موجود.. ابعت رسالة على الواتس 01221581154", 404

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
