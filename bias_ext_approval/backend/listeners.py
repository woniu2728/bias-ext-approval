from bias_core.extensions.runtime import (
    create_runtime_timeline_from_builder,
    get_runtime_user_by_id,
    notify_runtime_notification,
)


def handle_discussion_approved(event) -> None:
    admin_user = _resolve_user_or_none(event.admin_user_id)
    if admin_user is None:
        return

    notify_runtime_notification(
        "notify_discussion_approved_from_event",
        event=event,
        admin_user=admin_user,
        note=event.note,
    )
    create_runtime_timeline_from_builder(
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

    notify_runtime_notification(
        "notify_discussion_rejected_from_event",
        event=event,
        admin_user=admin_user,
        note=event.note,
    )
    create_runtime_timeline_from_builder(
        event,
        "discussion_review",
        extra={
            "actor_user_id": event.admin_user_id,
            "post_type": "discussionRejected",
        },
        update_discussion_last_post=False,
    )


def handle_discussion_resubmitted(event) -> None:
    create_runtime_timeline_from_builder(
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

    notify_runtime_notification(
        "notify_post_approved_from_event",
        event=event,
        admin_user=admin_user,
        note=event.note,
    )
    create_runtime_timeline_from_builder(
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

    notify_runtime_notification(
        "notify_post_rejected_from_event",
        event=event,
        admin_user=admin_user,
        note=event.note,
    )
    create_runtime_timeline_from_builder(
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
    create_runtime_timeline_from_builder(
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
        return get_runtime_user_by_id(user_id)
    except Exception:
        return None


