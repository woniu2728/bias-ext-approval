from __future__ import annotations

from bias_core.extensions import ResourceFieldDefinition


APPROVAL_POST_EVENT_TYPES = (
    "discussionApproved",
    "discussionRejected",
    "discussionResubmitted",
    "postApproved",
    "postRejected",
    "postResubmitted",
)


def count_discussion_pending_approvals(*args, **kwargs):
    return _service_method(get_runtime_service("content.discussions"), "count_pending_approvals")(*args, **kwargs)


def get_runtime_service(service_key: str, default=None):
    from bias_core.extensions.runtime import get_runtime_service as runtime_get_service

    return runtime_get_service(service_key, default)


def _service_method(service, name: str):
    if isinstance(service, dict):
        method = service.get(name)
    else:
        method = getattr(service, name, None)
    if not callable(method):
        raise RuntimeError(f"Approval 扩展运行时服务缺少方法: {name}")
    return method

def count_post_pending_approvals(*args, **kwargs):
    return _service_method(get_runtime_service("content.posts"), "count_pending_approvals")(*args, **kwargs)


def admin_stats_resource_field_definitions():
    return (
        ResourceFieldDefinition(
            resource="admin_stats",
            field="pendingApprovals",
            module_id="approval",
            resolver=resolve_admin_pending_approvals,
            description="后台统计中的待审核内容数量。",
        ),
    )


def resolve_admin_pending_approvals(stats, context: dict) -> int:
    return count_discussion_pending_approvals() + count_post_pending_approvals()


def resolve_approval_event_data(post, context: dict) -> dict | None:
    post_type = getattr(post, "type", "")
    if post_type not in APPROVAL_POST_EVENT_TYPES:
        return None

    parsed = _parse_approval_event_content(getattr(post, "content", ""))
    event_data = {
        "kind": post_type,
        "note": parsed["note"],
    }
    if parsed["previous_status"]:
        event_data["previous_status"] = parsed["previous_status"]
    if parsed["target_post_id"] is not None:
        event_data["target_post_id"] = parsed["target_post_id"]
    if parsed["target_post_number"] is not None:
        event_data["target_post_number"] = parsed["target_post_number"]
    return event_data


def _parse_approval_event_content(content: str | None) -> dict:
    note = ""
    previous_status = ""
    target_post_id = None
    target_post_number = None
    for line in _normalized_lines(content):
        if line.startswith("note:"):
            note = line.removeprefix("note:").strip()
        elif line.startswith("previous_status:"):
            previous_status = line.removeprefix("previous_status:").strip()
        elif line.startswith("target_post_id:"):
            raw_value = line.removeprefix("target_post_id:").strip()
            if raw_value.isdigit():
                target_post_id = int(raw_value)
        elif line.startswith("target_post_number:"):
            raw_value = line.removeprefix("target_post_number:").strip()
            if raw_value.isdigit():
                target_post_number = int(raw_value)

    return {
        "note": note,
        "previous_status": previous_status,
        "target_post_id": target_post_id,
        "target_post_number": target_post_number,
    }


def _normalized_lines(content: str | None) -> list[str]:
    return [
        line.strip()
        for line in (content or "").splitlines()
        if line.strip()
    ]

