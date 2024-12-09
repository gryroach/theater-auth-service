from pydantic import BaseModel


class RolePermissions(BaseModel):
    view_regular_movies: bool
    view_premium_movies: bool
    create_movies: bool
    edit_movies: bool
    delete_movies: bool


class Role(BaseModel):
    name: str
    permissions: RolePermissions

    def __str__(self):
        return self.name


class Roles:
    admin = Role(
        name="admin",
        permissions=RolePermissions(
            view_regular_movies=True,
            view_premium_movies=True,
            create_movies=True,
            edit_movies=True,
            delete_movies=True,
        ),
    )
    moderator = Role(
        name="moderator",
        permissions=RolePermissions(
            view_regular_movies=True,
            view_premium_movies=True,
            create_movies=True,
            edit_movies=True,
            delete_movies=False,
        ),
    )
    regular_user = Role(
        name="regular_user",
        permissions=RolePermissions(
            view_regular_movies=True,
            view_premium_movies=False,
            create_movies=False,
            edit_movies=False,
            delete_movies=False,
        ),
    )
    premium_user = Role(
        name="premium_user",
        permissions=RolePermissions(
            view_regular_movies=True,
            view_premium_movies=True,
            create_movies=False,
            edit_movies=False,
            delete_movies=False,
        ),
    )

    @classmethod
    def roles(cls):
        return [
            value.name for value in vars(cls).values()
            if isinstance(value, Role)
        ]
