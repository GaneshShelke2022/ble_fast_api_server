from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_current_user
from ..database import get_async_session
from ..services.device_service import list_devices, create_device, update_device, delete_device
from ..schemas.device_schema import DeviceCreate, DeviceOut
from ..utils.response import success_response, error_response

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("")
async def get_devices(db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    devs = await list_devices(db)
    return devs


@router.post("")
async def add_device(data: DeviceCreate, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    try:
        d = await create_device(db, **data.dict())
        return success_response("Device added", DeviceOut.from_orm(d).dict())
    except Exception as e:
        return error_response(str(e))


@router.put("/{device_id}")
async def edit_device(device_id: int, data: DeviceCreate, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    d = await update_device(db, device_id, **data.dict())
    if not d:
        raise HTTPException(status_code=404, detail="Device not found")
    return success_response("Device updated", DeviceOut.from_orm(d).dict())


@router.delete("/{device_id}")
async def remove_device(device_id: int, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    ok = await delete_device(db, device_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Device not found")
    return success_response("Device deleted", None)
