from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from geip.storage.database import init_db, crud
from geip.monitoring import alerts_logger

router = APIRouter()


class AlertCreate(BaseModel):
    type: str
    message: str
    severity: str = "medium"


class AlertUpdate(BaseModel):
    is_active: Optional[bool] = None
    message: Optional[str] = None


class AlertResponse(BaseModel):
    id: str
    type: str
    message: str
    severity: str
    is_active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


def init_alerts_on_startup():
    try:
        init_db()
        crud.init_alerts()
    except Exception as e:
        alerts_logger.error(f"Alert initialization failed: {e}")


@router.get("/active")
async def get_active_alerts():
    try:
        alerts = crud.get_active_alerts()
        alerts_logger.debug(f"Fetched {len(alerts)} active alerts")
        return {"alerts": alerts}
    except Exception as e:
        alerts_logger.error(f"Failed to fetch active alerts: {e}")
        return {"alerts": []}


@router.get("/")
async def get_all_alerts():
    try:
        alerts = crud.get_all_alerts()
        alerts_logger.debug(f"Fetched {len(alerts)} total alerts")
        return {"alerts": alerts}
    except Exception as e:
        alerts_logger.error(f"Failed to fetch all alerts: {e}")
        return {"alerts": []}


@router.get("/{alert_id}")
async def get_alert(alert_id: str):
    alert = crud.get_alert_by_id(alert_id)
    if not alert:
        alerts_logger.warning(f"Alert not found: {alert_id}")
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/")
async def create_alert(alert: AlertCreate):
    alerts_logger.info(f"Creating alert: {alert.type} - {alert.message}")
    new_alert = crud.create_alert(
        alert_type=alert.type,
        message=alert.message,
        severity=alert.severity,
    )
    alerts_logger.info(f"Alert created: {new_alert['id']}")
    return new_alert


@router.patch("/{alert_id}")
async def update_alert(alert_id: str, update: AlertUpdate):
    alerts_logger.info(f"Updating alert: {alert_id}")
    updated = crud.update_alert(
        alert_id=alert_id,
        is_active=update.is_active,
        message=update.message,
    )
    if not updated:
        alerts_logger.warning(f"Alert not found for update: {alert_id}")
        raise HTTPException(status_code=404, detail="Alert not found")
    alerts_logger.info(f"Alert updated: {alert_id}")
    return updated


@router.delete("/{alert_id}")
async def delete_alert(alert_id: str):
    alerts_logger.info(f"Deleting alert: {alert_id}")
    if not crud.delete_alert(alert_id):
        alerts_logger.warning(f"Alert not found for delete: {alert_id}")
        raise HTTPException(status_code=404, detail="Alert not found")
    alerts_logger.info(f"Alert deleted: {alert_id}")
    return {"status": "deleted"}
