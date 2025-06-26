def is_admin_or_self(current_user, target_user_id, admin_only=False):
    if admin_only:
        return current_user.role == "admin"
    return current_user.id == target_user_id or current_user.role == "admin"
