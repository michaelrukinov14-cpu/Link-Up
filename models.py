from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class ReportReasonEnum(str, enum.Enum):
    spam = "spam"
    fake = "fake"
    insults = "insults"
    content = "content"
    other = "other"


class TransactionTypeEnum(str, enum.Enum):
    stars_purchase = "stars_purchase"
    card_purchase = "card_purchase"
    premium_convert = "premium_convert"
    referral_bonus = "referral_bonus"
    refund = "refund"


class PremiumPlanEnum(str, enum.Enum):
    month = "month"
    year = "year"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("age >= 11", name="ck_users_age_min"),
        CheckConstraint("age <= 120", name="ck_users_age_max"),
        CheckConstraint("length(name) >= 1", name="ck_users_name_min"),
        CheckConstraint("length(name) <= 100", name="ck_users_name_max"),
        CheckConstraint("length(bio) <= 500", name="ck_users_bio_max"),
        Index("ix_users_city", "city"),
        Index("ix_users_gender", "gender"),
        Index("ix_users_is_active", "is_active"),
        Index("ix_users_is_premium", "is_premium"),
        Index("ix_users_lat_lon", "latitude", "longitude"),
        Index("ix_users_language", "language"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum), nullable=False)
    city: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    voice_file_id: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    language: Mapped[str] = mapped_column(String(8), nullable=False, default="ru")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    premium_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    crystal_balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    warn_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_banned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    search_gender: Mapped[Optional[GenderEnum]] = mapped_column(Enum(GenderEnum), nullable=True)
    search_age_min: Mapped[int] = mapped_column(Integer, nullable=False, default=18)
    search_age_max: Mapped[int] = mapped_column(Integer, nullable=False, default=99)
    search_max_distance: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    referral_code: Mapped[Optional[str]] = mapped_column(String(32), unique=True, nullable=True, index=True)
    referred_by: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="user", cascade="all, delete-orphan", order_by="Photo.position")
    sent_likes: Mapped[list["Like"]] = relationship("Like", foreign_keys="Like.from_user_id", back_populates="from_user", cascade="all, delete-orphan")
    received_likes: Mapped[list["Like"]] = relationship("Like", foreign_keys="Like.to_user_id", back_populates="to_user", cascade="all, delete-orphan")
    matches_as_user1: Mapped[list["Match"]] = relationship("Match", foreign_keys="Match.user1_id", back_populates="user1", cascade="all, delete-orphan")
    matches_as_user2: Mapped[list["Match"]] = relationship("Match", foreign_keys="Match.user2_id", back_populates="user2", cascade="all, delete-orphan")
    reports_sent: Mapped[list["Report"]] = relationship("Report", foreign_keys="Report.reporter_id", back_populates="reporter", cascade="all, delete-orphan")
    reports_received: Mapped[list["Report"]] = relationship("Report", foreign_keys="Report.reported_id", back_populates="reported")
    bans: Mapped[list["Ban"]] = relationship("Ban", foreign_keys="Ban.user_id", back_populates="user", cascade="all, delete-orphan")
    premiums: Mapped[list["Premium"]] = relationship("Premium", back_populates="user", cascade="all, delete-orphan")
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    crystal_transactions: Mapped[list["CrystalTransaction"]] = relationship("CrystalTransaction", back_populates="user", cascade="all, delete-orphan")
    referrals_given: Mapped[list["Referral"]] = relationship("Referral", foreign_keys="Referral.referrer_id", back_populates="referrer", cascade="all, delete-orphan")
    referrals_received: Mapped[list["Referral"]] = relationship("Referral", foreign_keys="Referral.referee_id", back_populates="referee", cascade="all, delete-orphan")


class Photo(Base):
    __tablename__ = "photos"
    __table_args__ = (
        CheckConstraint("position >= 0 AND position <= 2", name="ck_photos_position"),
        UniqueConstraint("user_id", "position", name="uq_photos_user_position"),
        Index("ix_photos_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_id: Mapped[str] = mapped_column(String(500), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="photos")


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("from_user_id", "to_user_id", name="uq_likes_from_to"),
        Index("ix_likes_from_user_id", "from_user_id"),
        Index("ix_likes_to_user_id", "to_user_id"),
        Index("ix_likes_is_mutual", "is_mutual"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    to_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    is_mutual: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    from_user: Mapped["User"] = relationship("User", foreign_keys=[from_user_id], back_populates="sent_likes")
    to_user: Mapped["User"] = relationship("User", foreign_keys=[to_user_id], back_populates="received_likes")


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("user1_id", "user2_id", name="uq_matches_user1_user2"),
        Index("ix_matches_user1_id", "user1_id"),
        Index("ix_matches_user2_id", "user2_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user1_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    user2_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user1: Mapped["User"] = relationship("User", foreign_keys=[user1_id], back_populates="matches_as_user1")
    user2: Mapped["User"] = relationship("User", foreign_keys=[user2_id], back_populates="matches_as_user2")


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        Index("ix_reports_reporter_id", "reporter_id"),
        Index("ix_reports_reported_id", "reported_id"),
        Index("ix_reports_is_reviewed", "is_reviewed"),
        Index("ix_reports_reason", "reason"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reporter_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    reported_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="SET NULL"), nullable=True)
    reason: Mapped[ReportReasonEnum] = mapped_column(Enum(ReportReasonEnum), nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_reviewed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    reporter: Mapped["User"] = relationship("User", foreign_keys=[reporter_id], back_populates="reports_sent")
    reported: Mapped[Optional["User"]] = relationship("User", foreign_keys=[reported_id], back_populates="reports_received")


class Ban(Base):
    __tablename__ = "bans"
    __table_args__ = (
        Index("ix_bans_user_id", "user_id"),
        Index("ix_bans_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    admin_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="bans")


class Premium(Base):
    __tablename__ = "premium"
    __table_args__ = (
        Index("ix_premium_user_id", "user_id"),
        Index("ix_premium_is_active", "is_active"),
        Index("ix_premium_expires_at", "expires_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    plan: Mapped[PremiumPlanEnum] = mapped_column(Enum(PremiumPlanEnum), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="premiums")


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_user_id", "user_id"),
        Index("ix_transactions_type", "type"),
        Index("ix_transactions_status", "status"),
        Index("ix_transactions_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    type: Mapped[TransactionTypeEnum] = mapped_column(Enum(TransactionTypeEnum), nullable=False)
    amount_stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    amount_crystals: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    amount_fiat: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    telegram_payment_charge_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    provider_payment_charge_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    payload: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="transactions")


class CrystalTransaction(Base):
    __tablename__ = "crystal_transactions"
    __table_args__ = (
        Index("ix_crystal_transactions_user_id", "user_id"),
        Index("ix_crystal_transactions_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(200), nullable=False)
    balance_after: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="crystal_transactions")


class Referral(Base):
    __tablename__ = "referrals"
    __table_args__ = (
        UniqueConstraint("referee_id", name="uq_referrals_referee"),
        Index("ix_referrals_referrer_id", "referrer_id"),
        Index("ix_referrals_referee_id", "referee_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    referrer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    referee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False)
    bonus_given: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    crystals_awarded: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    referrer: Mapped["User"] = relationship("User", foreign_keys=[referrer_id], back_populates="referrals_given")
    referee: Mapped["User"] = relationship("User", foreign_keys=[referee_id], back_populates="referrals_received")
