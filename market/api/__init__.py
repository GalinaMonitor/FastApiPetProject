from fastapi import APIRouter

from market.api import shop_unit

router = APIRouter()
router.include_router(shop_unit.router)