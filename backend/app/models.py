from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    role_name = Column(String, default="Member")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    violations = relationship("Violation", back_populates="user")
    bank_account = relationship("BankAccount", back_populates="user", uselist=False)
    tickets = relationship("Ticket", back_populates="user")
    submissions = relationship("ApplicationSubmission", back_populates="user")


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    permissions = relationship("OwnerPermission", back_populates="owner")


class OwnerPermission(Base):
    __tablename__ = "owner_permissions"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    key = Column(String, nullable=False)
    value = Column(Boolean, default=False)

    owner = relationship("Owner", back_populates="permissions")


class WebsiteSetting(Base):
    __tablename__ = "website_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)


class WebsitePage(Base):
    __tablename__ = "website_pages"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)


class WebsiteButton(Base):
    __tablename__ = "website_buttons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    color = Column(String, default="#3b82f6")
    position = Column(String, default="main")
    button_type = Column(String, default="page")
    href = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)


class WebsiteFeature(Base):
    __tablename__ = "website_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    color = Column(String, default="#3b82f6")
    is_active = Column(Boolean, default=True)


class Law(Base):
    __tablename__ = "laws"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    section = Column(String, default="General")
    is_active = Column(Boolean, default=True)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=True)
    button_color = Column(String, default="#3b82f6")
    icon = Column(String, default="📄")
    channel_id = Column(String, nullable=True)
    review_role_ids = Column(JSON, default=list)
    is_open = Column(Boolean, default=True)
    max_questions = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship("ApplicationQuestion", back_populates="application", cascade="all, delete-orphan")
    submissions = relationship("ApplicationSubmission", back_populates="application")


class ApplicationQuestion(Base):
    __tablename__ = "application_questions"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    question = Column(String, nullable=False)
    field_type = Column(String, default="short")
    required = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)

    application = relationship("Application", back_populates="questions")


class ApplicationSubmission(Base):
    __tablename__ = "application_submissions"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    payload = Column(JSON, default=dict)

    application = relationship("Application", back_populates="submissions")
    user = relationship("User", back_populates="submissions")


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type_name = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    amount = Column(Integer, default=0)
    officer_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_paid = Column(Boolean, default=False)
    payment_reference = Column(String, nullable=True)

    user = relationship("User", back_populates="violations")


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    account_name = Column(String, nullable=False)
    account_number = Column(String, nullable=False)
    balance = Column(Integer, default=0)
    total_deposit = Column(Integer, default=0)
    total_transfers = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="active")

    user = relationship("User", back_populates="bank_account")
    transactions = relationship("BankTransaction", back_populates="account")
    loans = relationship("Loan", back_populates="account")


class BankTransaction(Base):
    __tablename__ = "bank_transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Integer, default=0)
    description = Column(String, nullable=True)
    related_user_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("BankAccount", back_populates="transactions")


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("bank_accounts.id"), nullable=False)
    amount = Column(Integer, default=0)
    term_days = Column(Integer, default=30)
    remaining = Column(Integer, default=0)
    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("BankAccount", back_populates="loans")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ticket_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String, default="open")
    assigned_to = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="tickets")


class ServerLog(Base):
    __tablename__ = "server_logs"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    actor_name = Column(String, nullable=True)
    actor_discord_id = Column(String, nullable=True)
    target_name = Column(String, nullable=True)
    target_discord_id = Column(String, nullable=True)
    element_name = Column(String, nullable=True)
    description = Column(String, nullable=False)
    old_value = Column(String, nullable=True)
    new_value = Column(String, nullable=True)
    room_name = Column(String, nullable=True)
    system_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LoginSession(Base):
    __tablename__ = "login_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

