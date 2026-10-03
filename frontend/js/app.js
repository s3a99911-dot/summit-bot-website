# بوت القمة | SUMMIT BOT

منصة إلكترونية متكاملة ومتجاوبة لبوت القمة، مع واجهة احترافية وقاعدة بيانات منظمة، وتغطي:

- الصفحة الرئيسية
- صفحة المميزات
- صفحة المخالفات
- صفحة البنك
- صفحة التقديمات
- مركز اللوقات
- لوحة المالك
- إدارة الألوان والمحتوى
- دعم عربي / إنجليزي (هيكل جاهز)

## البنية

- `backend/app/` : تطبيق FastAPI
- `frontend/` : واجهة HTML/CSS/JS
- `requirements.txt` : متطلبات المشروع
- `.env.example` : متغيرات البيئة

## التشغيل السريع

```bash
python -m venv .venv
source .venv/bin/activate  # على Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

افتح المتصفح على:

- http://localhost:8000

## ملاحظات مهمة

- هذا المشروع جاهز كـ foundation متكامل ومشغل فعلي.
- تسجيل الدخول عبر Discord تم تركه كـ mock للاستخدام المحلي لعدم وجود OAuth حقيقي في البيئة الحالية.
- لإدماج OAuth2 الحقيقي، أضف قيم Discord في `.env` ثم استخدم مسار `/auth/discord` و `/auth/callback`.
- قاعدة البيانات الافتراضية: SQLite (`summit_bot.db`) ويمكن تغييرها إلى PostgreSQL داخل `.env`.

## المتغيرات الأساسية

```env
DATABASE_URL=sqlite:///./summit_bot.db
DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=
DISCORD_REDIRECT_URI=http://localhost:8000/auth/callback
SECRET_KEY=change-this-in-production
```

## التحسينات القادمة

- ربط حقيقي مع البوت Python عبر WebSocket وAPI
- إضافة OAuth2 حقيقي من Discord
- ربط PostgreSQL فعلي
- نظام جلسات آمنة بالتوكن
- نظام ملفات إعدادات للمالك
- دعم كامل لقوائم اللوقات والفلاتر

## ملاحظة

هذا الإصدار يوفر أساسًا حقيقيًا وقابلًا للتشغيل، مع بيانات تجريبية وبنية قابلة للتوسع لتصل إلى كامل متطلبات النظام المتكامل في طلبك.

