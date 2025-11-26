"""User controller for user management endpoints."""

from typing import Sequence

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData

from app.dtos.user import UserCreateDTO, UserReadDTO, UserUpdateDTO
from app.models import User
from app.repositories.user import UserRepository, provide_user_repo


class UserController(Controller):
    """Controller for user management operations."""

    path = "/users"
    dependencies = {"user_repo": Provide(provide_user_repo)}
    return_dto = UserReadDTO

    @get("/")
    async def list_users(
        self,
        user_repo: UserRepository,
    ) -> Sequence[User]:
        """List all users."""
        return user_repo.list()

    @get("/{user_id:int}")
    async def get_user(
        self,
        user_repo: UserRepository,
        user_id: int,
    ) -> User:
        """Get a user by ID."""
        return user_repo.get(user_id)

    @post("/", dto=UserCreateDTO, sync_to_thread=False, exclude_from_auth=True)  # ← AGREGAR exclude_from_auth=True
    async def create_user(
        self,
        user_repo: UserRepository,
        data: DTOData[User],
    ) -> User:
        """Create a new user."""
        return user_repo.add_with_hashed_password(data)

    @patch("/{user_id:int}", dto=UserUpdateDTO)
    async def update_user(
        self,
        user_repo: UserRepository,
        user_id: int,
        data: DTOData[User],
    ) -> User:
        """Update a user."""
        user, _ = user_repo.get_and_update(
            match_fields="id",
            id=user_id,
            **data.as_builtins(),
        )
        return user

    @delete("/{user_id:int}", status_code=204)
    async def delete_user(
        self,
        user_repo: UserRepository,
        user_id: int,
    ) -> None:
        """Delete a user."""
        user_repo.delete(user_id)