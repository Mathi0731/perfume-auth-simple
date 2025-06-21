from flask import Blueprint, render_template, request, current_app, render_template_string
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

        # Save to DB using PyMySQL
        conn = current_app.config["get_db_connection"]()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (brand, serial, mfg_date) VALUES (%s, %s, %s)",
                       (brand, serial, mfg_date))
        conn.commit()
        conn.close()

        # Generate QR
        qr_data = f"{brand}|{serial}|{mfg_date}"
        encoded = quote(qr_data)
        qr_url = f"https://your-project.up.railway.app/auto-verify?data={encoded}"  # Update URL!

        img = qrcode.make(qr_url)
        qr_path = f"{QR_FOLDER}/simple_{serial}.png"
        img.save(qr_path)

        return render_template('simple_result.html', qr_path=qr_path)

    return render_template('simple_add.html')


@simple.route('/auto-verify')
def auto_verify():
    try:
        qr_data = request.args.get('data')
        decoded = unquote(qr_data)
        brand, serial, mfg_date = decoded.split('|')

        conn = current_app.config["get_db_connection"]()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE serial=%s", (serial,))
        record = cursor.fetchone()
        conn.close()

        if record and record['brand'] == brand and str(record['mfg_date']) == mfg_date:
            result = "✅ Product is VALID"
        else:
            result = "❌ Product is FAKE or TAMPERED"
    except Exception as e:
        result = f"⚠️ Invalid QR Code or data: {str(e)}"

    return render_template_string(f"""
        <h2>Verification Result</h2>
        <p>{result}</p>
        <a href="/simple-add">← Add Another Product</a>
    """)
