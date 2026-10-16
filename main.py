import asyncio
import os
import random
import secrets
import socket
import struct
from urllib.parse import quote

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# تنظیمات از متغیرهای محیطی
SECRET = os.environ.get('SECRET', secrets.token_hex(16))
PORT = int(os.environ.get('PORT', '8443'))
SERVER_HOST = os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'localhost')

# ایجاد پورت داخلی برای پروکسی
PROXY_PORT = PORT + 1

# ذخیره اطلاعات پروکسی
proxy_info = {}

async def run_proxy_server():
    """اجرای سرور MTProto Proxy"""
    import mtprotoproxy

    # تنظیم کانفیگ
    mtprotoproxy.config_dict = {
        'PORTS': [PROXY_PORT],
        'USERS': {'default': {'secret': SECRET}},
        'TAG': 'MTProto Proxy',
        'LOG_LEVEL': 'INFO',
    }

    # اجرا
    await mtprotoproxy.main()

def get_external_ip():
    """دریافت IP خارجی سرور"""
    try:
        import requests
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text.strip()
    except:
        # اگه ipify جواب نداد، از دامنه Railway استفاده کن
        return SERVER_HOST

@app.on_event("startup")
async def startup_event():
    """شروع سرور هنگام راه‌اندازی"""
    ip = get_external_ip()
    secret_hex = SECRET.lower()

    proxy_info.update({
        'server': SERVER_HOST,
        'port': PORT,
        'secret': secret_hex,
        'ip': ip,
    })

    print(f"✅ Proxy Server started on {SERVER_HOST}:{PORT}")
    print(f"🔐 Secret: {secret_hex}")

@app.get("/", response_class=HTMLResponse)
async def root():
    """صفحه اصلی با لینک پروکسی"""
    info = proxy_info
    server = info.get('server', SERVER_HOST)
    port = info.get('port', PORT)
    secret = info.get('secret', SECRET).lower()
    ip = info.get('ip', SERVER_HOST)

    # لینک‌های اتصال
    proxy_link = f"tg://proxy?server={server}&port={port}&secret={secret}"
    proxy_link_ip = f"tg://proxy?server={ip}&port={port}&secret={secret}"

    # لینک HTTPS برای مرورگر
    https_link = f"https://{server}:{port}/"

    html = f'''
    <!DOCTYPE html>
    <html dir="rtl" lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🚀 تلگرام پروکسی MTProto</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Tahoma', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}

            .container {{
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 500px;
                width: 100%;
                padding: 40px;
            }}

            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 30px;
                font-size: 24px;
            }}

            .status {{
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
                font-weight: bold;
            }}

            .info-box {{
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
            }}

            .info-label {{
                color: #666;
                font-size: 14px;
                margin-bottom: 8px;
                font-weight: bold;
            }}

            .info-value {{
                background: #fff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                word-break: break-all;
                direction: ltr;
                text-align: left;
                position: relative;
            }}

            .copy-btn {{
                position: absolute;
                left: 10px;
                top: 50%;
                transform: translateY(-50%);
                background: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.3s;
            }}

            .copy-btn:hover {{
                background: #0056b3;
                transform: translateY(-50%) scale(1.05);
            }}

            .copy-btn.copied {{
                background: #28a745;
            }}

            .qr-section {{
                text-align: center;
                margin-top: 30px;
            }}

            .qr-link {{
                display: inline-block;
                background: #28a745;
                color: white;
                text-decoration: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                transition: all 0.3s;
            }}

            .qr-link:hover {{
                background: #218838;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(40, 167, 69, 0.3);
            }}

            .instructions {{
                background: #fff3cd;
                border: 1px solid #ffc107;
                color: #856404;
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                font-size: 13px;
                line-height: 1.8;
            }}

            .instructions strong {{
                display: block;
                margin-bottom: 10px;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 تلگرام پروکسی MTProto</h1>

            <div class="status">
                ✅ سرور فعال است
            </div>

            <div class="info-box">
                <div class="info-label">📡 سرور (Server)</div>
                <div class="info-value">
                    {server}
                    <button class="copy-btn" onclick="copyToClipboard('{server}', this)">کپی</button>
                </div>
            </div>

            <div class="info-box">
                <div class="info-label">🔌 پورت (Port)</div>
                <div class="info-value">
                    {port}
                    <button class="copy-btn" onclick="copyToClipboard('{port}', this)">کپی</button>
                </div>
            </div>

            <div class="info-box">
                <div class="info-label">🔐 سکرت (Secret)</div>
                <div class="info-value">
                    {secret}
                    <button class="copy-btn" onclick="copyToClipboard('{secret}', this)">کپی</button>
                </div>
            </div>

            <div class="info-box">
                <div class="info-label">🔗 لینک اتصال مستقیم</div>
                <div class="info-value">
                    {proxy_link}
                    <button class="copy-btn" onclick="copyToClipboard('{proxy_link}', this)">کپی</button>
                </div>
            </div>

            <div class="qr-section">
                <a href="{proxy_link}" class="qr-link">
                    📱 اتصال مستقیم در تلگرام
                </a>
            </div>

            <div class="instructions">
                <strong>📖 راهنمای اتصال:</strong>
                ۱. لینک بالا رو کپی کنید<br>
                ۲. در تلگرام به Settings → Data and Storage → Proxy Settings بروید<br>
                ۳. Add Proxy → MTProto رو انتخاب کنید<br>
                ۴. مقادیر رو وارد کنید یا لینک رو در مرورگر باز کنید
            </div>
        </div>

        <script>
            function copyToClipboard(text, btn) {{
                navigator.clipboard.writeText(text).then(() => {{
                    const originalText = btn.textContent;
                    btn.textContent = '✅ کپی شد';
                    btn.classList.add('copied');
                    setTimeout(() => {{
                        btn.textContent = originalText;
                        btn.classList.remove('copied');
                    }}, 2000);
                }}).catch(err => {{
                    alert('خطا در کپی کردن');
                }});
            }}
        </script>
    </body>
    </html>
    '''
    return html

@app.get("/info")
async def get_info():
    """دریافت اطلاعات پروکسی به صورت JSON"""
    return proxy_info

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
