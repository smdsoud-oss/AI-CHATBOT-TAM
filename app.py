import os
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from werkzeug.utils import secure_filename
from src.chatbot import chat
from functools import wraps
from flask import session
from src.pdf_reader import extract_text, summarize_text
from src.knowledge import (
    add_file_to_knowledge, add_manual_fact,
    get_all_knowledge, clear_knowledge_base,
    delete_knowledge_item
)
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, session, redirect

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'tam-secret-2026')
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect('/admin/login')
        return f(*args, **kwargs)
    return decorated

ALLOWED_EXTENSIONS = {
    'pdf', 'docx', 'doc',
    'xlsx', 'xls', 'csv',
    'pptx', 'ppt', 'txt'
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text = extract_text(filepath)
        if not text:
            return jsonify({'error': 'Could not read file'}), 400

        summary = summarize_text(text, max_chars=4000)
        return jsonify({
            'success': True,
            'filename': filename,
            'content': summary
        })

    return jsonify({'error': 'File type not supported'}), 400

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    user_message = data.get('message', '')
    file_content = data.get('file_content', None)

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        result, is_stream = chat(user_message, file_content)
    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'rate_limit' in error_msg.lower() or 'limit' in error_msg.lower():
            return jsonify({
                'response': '⏳ TAM has reached daily usage limits on all AI systems. Please try again in 30 minutes! — TAM 💡'
            })
        else:
            return jsonify({
                'response': '⚠️ TAM encountered an issue. Please try again! — TAM 💡'
            })

    if is_stream:
        return Response(
            stream_with_context(result),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )
    else:
        return jsonify({'response': result})
# ── ADMIN LOGIN ──

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.getenv('ADMIN_PASSWORD', 'soud@tam2026'):
            session.permanent = True
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            error = '❌ Wrong password! Try again.'
    return render_template('admin_login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin/login')

# ── ADMIN ROUTES ──

@app.route('/admin')
@admin_required
def admin_panel():
    return render_template('admin.html')

@app.route('/admin/upload_knowledge', methods=['POST'])
@admin_required
def upload_knowledge():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    category = request.form.get('category', 'general')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        success = add_file_to_knowledge(filepath, category)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Could not read file'}), 400

    return jsonify({'error': 'File type not supported'}), 400

@app.route('/admin/add_fact', methods=['POST'])
@admin_required
def add_fact():
    data = request.get_json()
    category = data.get('category', 'general')
    content = data.get('content', '')

    if content:
        add_manual_fact(category, content)
        return jsonify({'success': True})
    return jsonify({'error': 'No content provided'}), 400

@app.route('/admin/knowledge_list')
@admin_required
def knowledge_list():
    rows = get_all_knowledge()
    items = [
        {
            'id': item_id,
            'source': source,
            'category': category,
            'preview': content[:100]
        }
        for item_id, source, category, content in rows
    ]
    return jsonify({'items': items})

@app.route('/admin/delete_item', methods=['POST'])
@admin_required
def delete_item():
    data = request.get_json()
    item_id = data.get('id')
    print(f"Deleting item ID: {item_id}")
    if item_id is not None:
        delete_knowledge_item(item_id)
        return jsonify({'success': True})
    return jsonify({'error': 'No ID provided'}), 400

@app.route('/admin/clear_knowledge', methods=['POST'])
@admin_required
def clear_knowledge():
    clear_knowledge_base()
    return jsonify({'success': True})

@app.route('/ai_status')
def ai_status():
    from src.chatbot import get_current_ai
    return jsonify({'ai': get_current_ai()})


if __name__ == '__main__':
    app.run(debug=True)