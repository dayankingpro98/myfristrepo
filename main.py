import asyncio
import os
import secrets

# تنظیمات از متغیرهای محیطی
SECRET = os.environ.get('SECRET', secrets.token_hex(16)).lower()
PORT = int(os.environ.get('PORT', '8443'))

print(f"🚀 Starting MTProto Proxy")
print(f"📡 Port: {PORT}")
print(f"🔐 Secret: {SECRET}")

async def main():
    """اجرای پروکسی MTProto"""
    import mtprotoproxy

    # تنظیمات پروکسی
    mtprotoproxy.config_dict = {
        'PORTS': [PORT],
        'USERS': {
            'user': {
                'secret': SECRET
            }
        },
        'TAG': 'MTProto Proxy',
        'LOG_LEVEL': 'INFO',
        'MSG_PROXY': True,
    }

    # اجرا
    await mtprotoproxy.main()

if __name__ == '__main__':
    asyncio.run(main())
