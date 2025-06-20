from flask import Blueprint, render_template, request, current_app
import qrcode, os
from urllib.parse import quote, unquote

simple = Blueprint('simple', __name__)
QR_FOLDER = 'static/qrcodes'
os.makedirs(QR_FOLDER, exist_ok=True)

@simple.route('/simple-add', methods=['GET', 'POST'])
def simple_add():
    qr_path = None
    if request.method == 'POST':
        brand = request.form['brand']
        serial = request.form['serial']
        mfg_date = request.form['mfg_date']

        # Save to DB
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("INSERT INTO products (brand, serial, mfg_date) VALUES (%s, %s, %s)",
                       (brand, serial, mfg_date))
        current_app.mysql.connection.commit()

        # Create QR data as a URL
        qr_data = f"{brand}|{serial}|{mfg_date}"
        encoded = quote(qr_data)  # URL-safe
        qr_url = f"https://your-project.up.railway.app/auto-verify?data={encoded}"  # 🔁 Update this to match your Railway URL

        # Generate QR
        img = qrcode.make(qr_url)
        qr_path = f"{QR_FOLDER}/simple_{serial}.png"
        img.save(qr_path)

        return render_template('simple_result.html', qr_path=qr_path)

    return render_template('simple_add.html')


@simple.route('/auto-verify')
def auto_verify():
    from flask import render_template_string
    try:
        qr_data = request.args.get('data')
        decoded = unquote(qr_data)
        brand, serial, mfg_date = decoded.split('|')

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE serial=%s", (serial,))
        record = cursor.fetchone()

        if record and record[1] == brand and str(record[3]) == mfg_date:
            result = "✅ Product is VALID"
        else:
            result = "❌ Product is FAKE or TAMPERED"
    except:
        result = "⚠️ Invalid QR Code or data"

    return render_template_string(f"""
        <h2>Verification Result</h2>
        <p>{result}</p>
        <a href="/simple-add">← Add Another Product</a>
    """)
