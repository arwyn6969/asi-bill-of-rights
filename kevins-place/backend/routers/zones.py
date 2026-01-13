"""
Zone routes: List all zones, get specific zone.
"""

from typing import List

import sqlalchemy
from fastapi import APIRouter, HTTPException

from database import database, zones, threads
from schemas import ZoneResponse


router = APIRouter(prefix="/api/zones", tags=["Zones"])


@router.get("", response_model=List[ZoneResponse])
async def list_zones():
    """List all zones."""
    query = zones.select().order_by(zones.c.sort_order)
    zone_list = await database.fetch_all(query)
    
    result = []
    for zone in zone_list:
        # Count threads in zone
        count_query = sqlalchemy.select(sqlalchemy.func.count()).where(threads.c.zone_id == zone["id"])
        thread_count = await database.fetch_val(count_query) or 0
        
        result.append(ZoneResponse(
            id=zone["id"],
            name=zone["name"],
            description=zone["description"],
            icon=zone["icon"],
            allowed_types=zone["allowed_types"],
            thread_count=thread_count
        ))
    
    return result


@router.get("/{zone_id}", response_model=ZoneResponse)
async def get_zone(zone_id: str):
    """Get a specific zone."""
    query = zones.select().where(zones.c.id == zone_id)
    zone = await database.fetch_one(query)
    
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    count_query = sqlalchemy.select(sqlalchemy.func.count()).where(threads.c.zone_id == zone_id)
    thread_count = await database.fetch_val(count_query) or 0
    
    return ZoneResponse(
        id=zone["id"],
        name=zone["name"],
        description=zone["description"],
        icon=zone["icon"],
        allowed_types=zone["allowed_types"],
        thread_count=thread_count
    )
