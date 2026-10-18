from fastapi import HTTPException, status, Depends
from typing import List
from app.models.staff import StaffRole, Staff

# Dummy dependency to simulate current user retrieval
# This should be replaced with actual JWT verification and DB user retrieval
async def get_current_user() -> Staff:
    return None

def require_roles(allowed_roles: List[StaffRole]):
    def role_checker(current_user: Staff = Depends(get_current_user)):
        if current_user is None:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker
