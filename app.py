import os
from flask import Flask, render_template_string, request, jsonify, send_file
from pypdf import PdfReader

app = Flask(_name_)

PDF_PATH = "lesson1.pdf"
WHATSAPP_LINK = "https://wa.me/201221581154?s=t"
WHATSAPP_FALLBACK = f"الأسئلة مش موجودة حاليا.. تواصل معنا عبر الواتساب للاشتراك والنسخة الكاملة: {WHATSAPP_LINK}"

def extract_pdf_text(pdf_path):
    try:
        if not os.path.exists(pdf_path):
            return WHATSAPP_FALLBACK
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text if text.strip() else WHATSAPP_FALLBACK
    except Exception:
        return WHATSAPP_FALLBACK

@app.route('/')
def index():
    html_template = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>منصة سر التفوق التعليمية - العلوم المتكاملة</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f2c23; margin: 0; padding: 15px; color: #fff; min-height: 100vh; display: flex; justify-content: center; align-items: center; }
            .container { width: 100%; max-width: 600px; background: #133a2e; padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); border: 1px solid #1a4d3e; }
            .brand-badge { background: #1b4d3e; color: #f1c40f; display: inline-block; padding: 6px 18px; border-radius: 20px; font-weight: bold; font-size: 13px; margin-bottom: 12px; border: 1px solid #276953; text-align: center; width: fit-content; margin-left: auto; margin-right: auto; }
            .brand-header { text-align: center; margin-bottom: 20px; }
            .edition-tag { color: #a3e4d7; font-size: 13px; font-weight: bold; margin-bottom: 8px; }
            h1 { color: #ffffff; margin: 5px 0 15px 0; font-size: 20px; line-height: 1.5; font-weight: bold; }
            .desc { color: #cbd5e1; font-size: 13px; line-height: 1.6; margin-bottom: 15px; text-align: center; }
            .whatsapp-banner { color: #ffffff; font-size: 13px; font-weight: bold; margin-bottom: 20px; text-align: center; }
            .whatsapp-btn-container { text-align: center; margin-bottom: 25px; }
            .whatsapp-btn { background: #27ae60; color: white; text-decoration: none; display: inline-block; padding: 14px 28px; border-radius: 30px; font-weight: bold; font-size: 15px; box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4); transition: transform 0.2s; }
            .whatsapp-btn:hover { transform: scale(1.02); background: #219653; }
            
            .meta-section { background: #0f2c23; padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #1a4d3e; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }
            .meta-title { color: #2ecc71; font-weight: bold; font-size: 14px; }
            .meta-features { display: flex; gap: 15px; font-size: 12px; color: #cbd5e1; justify-content: center; width: 100%; margin-top: 10px; border-top: 1px solid #1a4d3e; padding-top: 10px; }
            
            .chat-box { height: 300px; border: 1px solid #1a4d3e; border-radius: 12px; padding: 15px; overflow-y: scroll; background: #0b221a; margin-bottom: 15px; display: flex; flex-direction: column; gap: 10px; }
            .message { padding: 10px 14px; border-radius: 10px; max-width: 85%; line-height: 1.5; font-size: 14px; }
            .user-msg { background: #2980b9; color: white; align-self: flex-start; }
            .ai-msg { background: #1a4d3e; color: #ecf0f1; align-self: flex-end; border: 1px solid #276953; }
            
            .input-area { display: flex; gap: 10px; }
            input[type="text"] { flex: 1; padding: 12px; border: 1px solid #276953; border-radius: 10px; font-size: 14px; outline: none; background: #0b221a; color: white; }
            input[type="text"]:focus { border-color: #2ecc71; }
            button { background: #27ae60; color: white; border: none; padding: 12px 22px; border-radius: 10px; font-size: 14px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
            button:hover { background: #219653; }
            
            .pdf-link-container { text-align: center; margin-bottom: 15px; }
            .pdf-link { color: #a3e4d7; text-decoration: none; font-size: 13px; font-weight: bold; }
            .pdf-link:hover { text-decoration: underline; }
            .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #7f8c8d; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="brand-header">
                <div class="brand-badge">سر التفوق</div>
                <div class="edition-tag">النسخة الكاملة</div>
                <h1>الدرس الأول مجرد بداية.. جاهز تتحدى نفسك وتكتشف سر التفوق الحقيقي في باقي المنهج؟ 👑</h1>
                <div class="desc">لا تكتف بدرس واحد! انضم للنسخة الكاملة، وفك قفل بقية الدروس لإنشاء امتحانات لا نهائية متجددة مع تصحيح فوري وشرح لكل سؤال.</div>
                <div class="whatsapp-banner">التواصل عبر الواتساب فقط: 01221581154</div>
            </div>
            
            <div class="whatsapp-btn-container">
                <a href="https://wa.me/201221581154?s=t" target="_blank" class="whatsapp-btn">
                    💬 تواصل عبر الواتساب فقط للاشتراك
                </a>
            </div>

            <div class="meta-section">
                <div class="meta-title">🟢 مادة العلوم المتكاملة لسنة تانية بكالوريا 2027</div>
                <div style="font-size: 12px; color: #f39c12; font-weight: bold;">FREE DEMO</div>
                <div class="meta-features">
                    <span>♾️ نماذج متجددة (بدون أسئلة ثابتة)</span>
                    <span>✔️ تصحيح فوري (مع تفسير وتحسين)</span>
                    <span>⏱️ تدريب مركز (على نفس المحتوى)</span>
                </div>
            </div>

            <div class="pdf-link-container">
                <a href="/view-pdf" target="_blank" class="pdf-link">📄 استعرض ملف الدرس الأصلي (PDF) للتدريب</a>
            </div>

            <div class="chat-box" id="chatBox">
                <div class="message ai-msg">أهلاً بك يا بطل في منصة <b>سر التفوق</b>! 🎓 اسألني أي سؤال بخصوص محتوى الدرس الأول في العلوم المتكاملة وسأجيبك فوراً!</div>
            </div>

            <div class="input-area">
                <input type="text" id="userInput" placeholder="اكتب سؤالك هنا بخصوص الدرس..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">إرسال</button>
            </div>
            
            <div class="footer">
                جميع الحقوق محفوظة © سر التفوق 2027
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
                    appendMessage(data.answer || 'للاشتراك وتفاصيل المنهج الكامل، تواصل معنا عبر الواتساب: https://wa.me/201221581154?s=t', 'ai');
                } catch (e) {
                    document.getElementById(loadingId).remove();
                    appendMessage('للاشتراك تواصل معنا عبر الواتساب: https://wa.me/201221581154?s=t', 'ai');
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
    
    # رد ذكي وتوجيه فوري للواتساب لضمان عدم حدوث أي تعطل نهائياً
    answer = f"أهلاً بك يا بطل! بناءً على سؤالك حول '{question}'، يمكنك متابعة الشرح الكامل وحل جميع الأسئلة بالانضمام للنسخة الكاملة عبر الواتساب: https://wa.me/201221581154?s=t"
    return jsonify({'answer': answer})

@app.route('/view-pdf')
def view_pdf():
    if os.path.exists(PDF_PATH):
        return send_file(PDF_PATH)
    return "الملف غير موجود.. تواصل عبر الواتساب: https://wa.me/201221581154?s=t", 404

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
