def get_runtime_service(service_key: str, default=None):
    from bias_core.extensions.runtime import get_runtime_service as runtime_get_service

    return runtime_get_service(service_key, default)


def _service_method(service, name: str, *, required: bool = True):
    if isinstance(service, dict):
        method = service.get(name)
    else:
        method = getattr(service, name, None)
    if callable(method):
        return method
    if required:
        raise RuntimeError(f"Approval 扩展运行时服务缺少方法: {name}")
    return None


def _call_notification(method_name: str, **kwargs):
    service = get_runtime_service("notifications.service")
    method = _service_method(service, method_name, required=False) if service is not None else None
    if method is not None:
        return method(**kwargs)


def _create_timeline_from_builder(*args, **kwargs):
    return _service_method(get_runtime_service("discussions.timeline"), "create_from_builder")(*args, **kwargs)


def handle_discussion_approved(event) -> None:
    admin_user = _resolve_user_or_none(event.admin_user_id)
    if admin_user is None:
        return

    _call_notification(
        "notify_discussion_approved_from_event",
        event=event,
        admin_user=admin_user,
        note=event.note,
    )
    _create_timeline_from_builder(
        event,
        "discussion_review",
        extra={
            "actor_user_id": event.admin_user_id,
            "post_type": "discussionApproved",
            "previous_status": "pending",
        },
        update_discussion_last_post=False,
    )


def handle_discussion_rejected(event) -> None:
    admin_user = _resolve_user_or_none(event.admin_user_id)
    if admin_user is None:
        return

    _call_notification(
        "notify_discussion_rejected_from_event",
        event=event,
        admin_user=admin_user,
        note=event.note,
    )
    _create_timeline_from_builder(
        event,
        "discussion_review",
        extra={
            "actor_user_id": event.admin_user_id,
            "post_type": "discussionRejected",
        },
        update_discussion_last_post=False,
    )


def handle_discussion_resubmitted(event) -> None:
    _create_timeline_from_builder(
        event,
        "discussion_resubmitted",
        extra={
            "post_type": "discussionResubmitted",
        },
        update_discussion_last_post=False,
    )


def handle_post_approved(event) -> None:
    admin_user = _resolve_user_or_none(event.admin_user_id)
    if admin_user is None:
        return

    _call_notification(
        "notify_post_approved_from_event",
        event=event,
        admin_user=admin_user,
        note=event.note,
    )
    _create_timeline_from_builder(
        event,
        "post_review",
        extra={
            "actor_user_id": event.admin_user_id,
            "post_type": "postApproved",
            "post_number": getattr(event, "post_number", None),
        },
        update_discussion_last_post=False,
    )


def handle_post_rejected(event) -> None:
    admin_user = _resolve_user_or_none(event.admin_user_id)
    if admin_user is None:
        return

    _call_notification(
        "notify_post_rejected_from_event",
        event=event,
        admin_user=admin_user,
        note=event.note,
    )
    _create_timeline_from_builder(
        event,
        "post_review",
        extra={
            "actor_user_id": event.admin_user_id,
            "post_type": "postRejected",
            "post_number": getattr(event, "post_number", None),
        },
        update_discussion_last_post=False,
    )


def handle_post_resubmitted(event) -> None:
    _create_timeline_from_builder(
        event,
        "post_resubmitted",
        extra={
            "post_type": "postResubmitted",
            "post_number": getattr(event, "post_number", None),
        },
        update_discussion_last_post=False,
    )


def _resolve_user_or_none(user_id: int):
    try:
        return _service_method(get_runtime_service("users.service"), "get_by_id")(user_id)
    except Exception:
        return None


