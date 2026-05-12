import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from geip.storage.database import AlertModel, SessionLocal


def get_db_session():
    return SessionLocal()


def create_alert(alert_type: str, message: str, severity: str) -> dict:
    db = get_db_session()
    try:
        alert = AlertModel(
            id=str(uuid.uuid4()),
            type=alert_type,
            message=message,
            severity=severity,
            is_active=True,
            created_at=datetime.utcnow(),
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert.to_dict()
    finally:
        db.close()


def get_active_alerts() -> list[dict]:
    db = get_db_session()
    try:
        alerts = db.query(AlertModel).filter(AlertModel.is_active == True).all()
        return [a.to_dict() for a in alerts]
    finally:
        db.close()


def get_all_alerts() -> list[dict]:
    db = get_db_session()
    try:
        alerts = db.query(AlertModel).order_by(AlertModel.created_at.desc()).all()
        return [a.to_dict() for a in alerts]
    finally:
        db.close()


def get_alert_by_id(alert_id: str) -> Optional[dict]:
    db = get_db_session()
    try:
        alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
        return alert.to_dict() if alert else None
    finally:
        db.close()


def update_alert(alert_id: str, is_active: Optional[bool] = None, message: Optional[str] = None) -> Optional[dict]:
    db = get_db_session()
    try:
        alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
        if not alert:
            return None
        
        if is_active is not None:
            alert.is_active = is_active
        if message is not None:
            alert.message = message
        
        alert.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(alert)
        return alert.to_dict()
    finally:
        db.close()


def delete_alert(alert_id: str) -> bool:
    db = get_db_session()
    try:
        alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
        if not alert:
            return False
        db.delete(alert)
        db.commit()
        return True
    finally:
        db.close()


def init_alerts():
    db = get_db_session()
    try:
        count = db.query(AlertModel).count()
        if count == 0:
            default_alerts = [
                AlertModel(
                    id=str(uuid.uuid4()),
                    type="price",
                    message="WTI crossed $80 threshold",
                    severity="medium",
                    is_active=True,
                    created_at=datetime.utcnow(),
                ),
                AlertModel(
                    id=str(uuid.uuid4()),
                    type="risk",
                    message="High risk detected in Strait of Hormuz",
                    severity="high",
                    is_active=True,
                    created_at=datetime.utcnow(),
                ),
            ]
            for alert in default_alerts:
                db.add(alert)
            db.commit()
    finally:
        db.close()
