from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models
from .database import get_db, init_db
from datetime import datetime
import logging

# Initialize database
init_db()

app = FastAPI(title="IP Reverser API", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reverse_ip(ip: str) -> str:
    """Reverse the IP address"""
    return ".".join(ip.split(".")[::-1])


@app.get("/")
async def get_reverse_ip(request: Request, db: Session = Depends(get_db)):
    """Get client IP, reverse it, and store in database"""

    # Get client IP from request
    client_ip = request.client.host
    logger.info(f"Received request from IP: {client_ip}")

    if not client_ip:
        raise HTTPException(status_code=400, detail="Could not determine client IP")

    # Reverse the IP
    reversed_ip = reverse_ip(client_ip)
    logger.info(f"Reversed IP: {reversed_ip}")

    # Create database record
    db_record = models.ReverseIP(original_ip=client_ip, reversed_ip=reversed_ip)

    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return {
        "original_ip": client_ip,
        "reversed_ip": reversed_ip,
        "record_id": db_record.id,
    }


@app.get("/history")
async def get_history(db: Session = Depends(get_db)):
    """Get all stored IP reversal records"""
    records = (
        db.query(models.ReverseIP).order_by(models.ReverseIP.created_at.desc()).all()
    )

    return [
        {
            "id": record.id,
            "original_ip": record.original_ip,
            "reversed_ip": record.reversed_ip,
            "created_at": record.created_at.isoformat(),
        }
        for record in records
    ]


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
