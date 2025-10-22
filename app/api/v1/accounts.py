from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...api.deps import get_current_user
from ...models.user import User
from ...schemas.account import AccountCreate, AccountResponse
from ...services.account_service import AccountService

router = APIRouter()

@router.post("/", response_model=AccountResponse)
def create_account(
    account: AccountCreate,
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)):
    service=AccountService(db)
    return service.create_account(user_id=current_user.id, account_data=account)

@router.get("/", response_model=List[AccountResponse])
def list_accounts(
    db: Session=Depends(get_db),
    current_user: User=Depends(get_current_user)):
    service=AccountService(db)
    return service.get_accounts_by_user(user_id=current_user.id)

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = AccountService(db)
    account = service.get_account_by_id(account_id, current_user.id)
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    return account
