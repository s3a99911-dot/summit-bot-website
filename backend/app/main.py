from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from backend.app.config import BASE_DIR, FRONTEND_DIR, settings
from backend.app.database import Base, SessionLocal, engine
from backend.app.models import (
    Application,
    ApplicationQuestion,
    BankAccount,
    BankTransaction,
    Law,
    LoginSession,
    Owner,
    OwnerPermission,
    ServerLog,
    User,
    Violation,
    WebsiteButton,
    WebsiteFeature,
    WebsitePage,
    WebsiteSetting,
)

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_data(db: Session):
    if db.query(WebsiteSetting).count() == 0:
        db.add_all(
            [
                WebsiteSetting(key="site_name", value="بوت القمة | SUMMIT BOT"),
                WebsiteSetting(key="primary_color", value="#3b82f6"),
                WebsiteSetting(key="background_color", value="#0f172a"),
                WebsiteSetting(key="button_color", value="#5865f2"),
                WebsiteSetting(key="card_color", value="#111827"),
                WebsiteSetting(key="text_color", value="#e5e7eb"),
                WebsiteSetting(key="hero_title", value="بوت القمة"),
                WebsiteSetting(key="hero_description", value="منصة متكاملة لإدارة المخالفات، البنك، التقديمات، اللوقات واللوحة الإدارية."),
                WebsiteSetting(key="discord_server_url", value="https://discord.gg/example"),
            ]
        )

    if db.query(WebsiteFeature).count() == 0:
        db.add_all(
            [
                WebsiteFeature(name="نظام المخالفات", description="إدارة المخالفات، الدفع، والمتابعة اللحظية.", icon="🚨", color="#ef4444"),
                WebsiteFeature(name="النظام البنكي", description="الحسابات، التحويلات، القروض وتسديدها.", icon="💳", color="#10b981"),
                WebsiteFeature(name="التقديمات", description="إنشاء التقديمات، طلبات التقديم، والمراجعة.", icon="📝", color="#f59e0b"),
                WebsiteFeature(name="التذاكر", description="إدارة التذاكر والردود من لوحة المالك.", icon="🎫", color="#8b5cf6"),
                WebsiteFeature(name="اللوقات", description="مراقبة كل حدث داخل السيرفر.", icon="🧭", color="#38bdf8"),
            ]
        )

    if db.query(WebsiteButton).count() == 0:
        db.add_all(
            [
                WebsiteButton(name="الرئيسية", description="مقدمة الموقع", icon="🏠", color="#3b82f6", position="nav", button_type="page", href="#home"),
                WebsiteButton(name="المميزات", description="مزايا البوت", icon="✨", color="#60a5fa", position="nav", button_type="page", href="#features"),
                WebsiteButton(name="المخالفات", description="مخالفاتك", icon="⚠️", color="#ef4444", position="nav", button_type="page", href="#violations"),
                WebsiteButton(name="البنك", description="أنشطتك البنكية", icon="💰", color="#10b981", position="nav", button_type="page", href="#bank"),
                WebsiteButton(name="التقديمات", description="التقديمات المتاحة", icon="🧾", color="#f59e0b", position="nav", button_type="page", href="#applications"),
            ]
        )

    if db.query(Law).count() == 0:
        db.add_all(
            [
                Law(title="قوانين الإدارة", summary="أساسيات السلوك داخل مجتمع السيرفر", content="يجب الالتزام بأخلاقيات الإدارة، وعدم التحيز، واحترام جميع الأعضاء.", section="إدارة"),
                Law(title="قوانين الأعضاء", summary="ضوابط المشاركة", content="الحفاظ على الأدب، وعدم السخرية، وعدم استخدام الرسائل المسيئة أو الترويج غير المصرح به.", section="أعضاء"),
                Law(title="قوانين التقديمات", summary="شروط التقديم", content="يجب تعبئة جميع الحقول المطلوبة بدقة، والالتزام بالمتطلبات المفروضة.", section="تقديمات"),
            ]
        )

    if db.query(User).count() == 0:
        user1 = User(discord_id="1542167442023915543", username="s3a99911-dot", avatar="https://cdn.discordapp.com/avatars/1542167442023915543/a.png", is_verified=True, role_name="Owner")
        user2 = User(discord_id="100000000000000001", username="PlayerOne", avatar="https://cdn.discordapp.com/embed/avatars/0.png", is_verified=True, role_name="Member")
        user3 = User(discord_id="100000000000000002", username="GamerX", avatar="https://cdn.discordapp.com/embed/avatars/1.png", is_verified=True, role_name="Moderator")
        db.add_all([user1, user2, user3])
        db.flush()

        db.add_all(
            [
                Violation(user_id=user2.id, type_name="مخالفة إدارية", reason="عدم الالتزام بقواعد المحادثة", amount=150, officer_name="Owner", is_paid=False),
                Violation(user_id=user2.id, type_name="مخالفة بنكية", reason="تجاوز في نظام الرسوم", amount=200, officer_name="Owner", is_paid=True, payment_reference="REF-101"),
                BankAccount(user_id=user2.id, account_name="PlayerOne", account_number="BK-1001", balance=9500, total_deposit=26000, total_transfers=1800, is_active=True, status="active"),
                BankAccount(user_id=user3.id, account_name="GamerX", account_number="BK-1002", balance=13500, total_deposit=28000, total_transfers=6500, is_active=True, status="active"),
                ServerLog(event_type="member.join", actor_name="System", description="عضو جديد انضم إلى السيرفر", room_name="general", system_name="Discord"),
                ServerLog(event_type="violation.add", actor_name="Admin", description="تم إضافة مخالفة جديدة", room_name="mod-logs", system_name="SUMMIT BOT"),
                ServerLog(event_type="bank.transfer", actor_name="PlayerOne", description="تم تحويل مبلغ", room_name="bank", system_name="SUMMIT BOT"),
            ]
        )

    if db.query(Owner).count() == 0:
        owner = Owner(discord_id="1542167442023915543", username="s3a99911-dot", avatar="https://cdn.discordapp.com/avatars/1542167442023915543/a.png", is_primary=True, is_active=True)
        db.add(owner)
        db.flush()
        db.add_all(
            [
                OwnerPermission(owner_id=owner.id, key="dashboard_view", value=True),
                OwnerPermission(owner_id=owner.id, key="logs_view", value=True),
                OwnerPermission(owner_id=owner.id, key="owners_manage", value=True),
                OwnerPermission(owner_id=owner.id, key="applications_manage", value=True),
                OwnerPermission(owner_id=owner.id, key="bank_manage", value=True),
                OwnerPermission(owner_id=owner.id, key="violations_manage", value=True),
                OwnerPermission(owner_id=owner.id, key="theme_manage", value=True),
            ]
        )

    db.commit()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.app_name, "environment": settings.app_env}


@app.get("/api/overview")
def overview(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_violations = db.query(Violation).count()
    total_bank_accounts = db.query(BankAccount).count()
    total_logs = db.query(ServerLog).count()
    total_owners = db.query(Owner).count()
    total_applications = db.query(Application).count()
    total_tickets = 0

    return {
        "site_name": "بوت القمة | SUMMIT BOT",
        "bot_status": "Online",
        "guild_members": total_users,
        "violations": total_violations,
        "bank_accounts": total_bank_accounts,
        "applications": total_applications,
        "tickets": total_tickets,
        "logs": total_logs,
        "owners": total_owners,
        "operations": 128,
        "updated_at": datetime.utcnow().isoformat(),
    }


@app.get("/api/features")
def features(db: Session = Depends(get_db)):
    return [{
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "icon": item.icon,
        "color": item.color,
    } for item in db.query(WebsiteFeature).filter(WebsiteFeature.is_active == True).all()]


@app.get("/api/violations")
def violations(discord_id: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Violation)
    if discord_id:
        user = db.query(User).filter(User.discord_id == discord_id).first()
        if user:
            query = query.filter(Violation.user_id == user.id)
    items = query.order_by(Violation.id.desc()).all()
    payload = []
    for item in items:
        payload.append({
            "id": item.id,
            "type": item.type_name,
            "reason": item.reason,
            "amount": item.amount,
            "officer": item.officer_name,
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "status": "مدفوعة" if item.is_paid else "غير مدفوعة",
            "is_paid": item.is_paid,
        })
    return payload


@app.get("/api/bank/{discord_id}")
def user_bank(discord_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.discord_id == discord_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    account = db.query(BankAccount).filter(BankAccount.user_id == user.id).first()
    if not account:
        return {
            "account": None,
            "balance": 0,
            "transactions": [],
        }

    transactions = db.query(BankTransaction).filter(BankTransaction.account_id == account.id).order_by(BankTransaction.id.desc()).all()
    return {
        "account": {
            "name": account.account_name,
            "number": account.account_number,
            "balance": account.balance,
            "total_deposit": account.total_deposit,
            "total_transfers": account.total_transfers,
            "status": account.status,
            "is_active": account.is_active,
        },
        "balance": account.balance,
        "transactions": [
            {
                "id": t.id,
                "type": t.transaction_type,
                "amount": t.amount,
                "description": t.description,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in transactions
        ],
    }


@app.get("/api/applications")
def applications(db: Session = Depends(get_db)):
    rows = db.query(Application).order_by(Application.id.desc()).all()
    result = []
    for item in rows:
        result.append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "image": item.image,
            "button_color": item.button_color,
            "icon": item.icon,
            "is_open": item.is_open,
            "questions": [
                {
                    "id": q.id,
                    "question": q.question,
                    "field_type": q.field_type,
                    "required": q.required,
                    "order": q.order_index,
                }
                for q in sorted(item.questions, key=lambda x: x.order_index)
            ],
        })
    return result


@app.get("/api/logs")
def logs(window: str = "7d", db: Session = Depends(get_db)):
    query = db.query(ServerLog).order_by(ServerLog.id.desc())
    rows = query.all()
    return [{
        "id": item.id,
        "event_type": item.event_type,
        "actor_name": item.actor_name,
        "actor_discord_id": item.actor_discord_id,
        "target_name": item.target_name,
        "target_discord_id": item.target_discord_id,
        "element_name": item.element_name,
        "description": item.description,
        "room_name": item.room_name,
        "system_name": item.system_name,
        "created_at": item.created_at.isoformat() if item.created_at else None,
    } for item in rows[:30]]


@app.get("/api/owners")
def owners(db: Session = Depends(get_db)):
    items = db.query(Owner).all()
    return [{
        "id": item.id,
        "discord_id": item.discord_id,
        "username": item.username,
        "avatar": item.avatar,
        "is_primary": item.is_primary,
        "is_active": item.is_active,
        "permissions": [
            {"key": p.key, "value": p.value}
            for p in item.permissions
        ],
    } for item in items]


@app.get("/api/laws")
def laws(db: Session = Depends(get_db)):
    items = db.query(Law).filter(Law.is_active == True).all()
    return [{
        "id": item.id,
        "title": item.title,
        "summary": item.summary,
        "content": item.content,
        "section": item.section,
    } for item in items]


@app.post("/api/settings/theme")
def update_theme(payload: dict):
    return {"status": "ok", "message": "تم حفظ ألوان الموقع بنجاح", "payload": payload}


@app.post("/api/settings/content")
def update_content(payload: dict):
    return {"status": "ok", "message": "تم حفظ محتوى الموقع بنجاح", "payload": payload}


@app.post("/api/owners")
def add_owner(payload: dict):
    return {"status": "ok", "message": "تم إضافة مالك جديد بنجاح", "payload": payload}


@app.get("/auth/discord")
def discord_login():
    if not settings.discord_client_id:
        return JSONResponse({"status": "mock", "message": "تمت محاكاة تسجيل الدخول عبر Discord لبيئة التطوير. أضف OAuth2 الحقيقي في ملف .env."})

    params = {
        "client_id": settings.discord_client_id,
        "redirect_uri": settings.discord_redirect_uri,
        "response_type": "code",
        "scope": "identify guilds",
    }
    return {"url": "https://discord.com/oauth2/authorize?" + "&".join(f"{k}={v}" for k, v in params.items())}


@app.get("/auth/callback")
def discord_callback(code: str | None = None):
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")
    return {
        "status": "ok",
        "message": "تم تسجيل الدخول بنجاح (محاكاة) - استبدل هذا الرابط باستخدام OAuth2 الحقيقي في الإنتاج.",
        "discord_id": "1542167442023915543",
        "username": "s3a99911-dot",
        "avatar": "https://cdn.discordapp.com/avatars/1542167442023915543/a.png",
    }


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
