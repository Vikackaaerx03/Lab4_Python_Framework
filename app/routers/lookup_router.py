from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.db.database import get_lookups_collection
from app.models.lookup_models import HistoryResponse, IpLookupCreate, LookupResponse
from app.repositories.lookup_repository import LookupRepository
from app.services.lookup_service import LookupService

router = APIRouter(prefix="/ip", tags=["IP Lookup"])


def get_lookup_service(lookups_collection=Depends(get_lookups_collection)) -> LookupService:
    return LookupService(LookupRepository(lookups_collection))


@router.post("/lookup", response_model=LookupResponse)
def lookup_ip(
    payload: IpLookupCreate,
    current_user: dict = Depends(get_current_user),
    service: LookupService = Depends(get_lookup_service),
):
    return service.lookup_ip(payload, current_user)


@router.get("/history", response_model=HistoryResponse)
def lookup_history(
    current_user: dict = Depends(get_current_user),
    service: LookupService = Depends(get_lookup_service),
):
    return service.history(current_user)
