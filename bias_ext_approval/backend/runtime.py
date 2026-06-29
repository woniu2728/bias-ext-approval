from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import transaction

from bias_core.extensions.runtime import (
    list_runtime_discussion_approval_queue_items,
    list_runtime_post_approval_queue_items,
    process_runtime_discussion_approval_item,
    process_runtime_post_approval_item,
)


def approval_service_provider() -> dict:
    return {
        "serialize_item": serialize_approval_item,
        "list_queue": list_approval_queue_items,
        "process_item": process_approval_item,
        "bulk_process": bulk_process_approval_items,
    }


def serialize_approval_item(content_type: str, item) -> dict:
    if isinstance(item, dict):
        return dict(item)
    raise ValidationError("审核项必须由内容扩展序列化")


def list_approval_queue_items(*, content_type: str = "all") -> list[dict]:
    items = []

    if content_type in {"all", "discussion"}:
        items.extend(list_runtime_discussion_approval_queue_items())

    if content_type in {"all", "post"}:
        items.extend(list_runtime_post_approval_queue_items())

    items.sort(key=lambda item: item["created_at"], reverse=True)
    return items


def process_approval_item(*, content_type: str, content_id: int, action: str, actor, note: str = "") -> dict:
    normalized_type = str(content_type or "").strip()
    normalized_action = str(action or "").strip()
    if normalized_type == "discussion":
        return _process_discussion_approval(content_id, normalized_action, actor, note)
    if normalized_type == "post":
        return _process_post_approval(content_id, normalized_action, actor, note)
    raise ValidationError("无效的审核内容类型")


def bulk_process_approval_items(*, action: str, items, actor, note: str = "") -> list[dict]:
    if action not in {"approve", "reject"}:
        raise ValidationError("无效的审核动作")
    if not isinstance(items, list) or not items:
        raise ValidationError("请至少选择一条待审核内容")

    processed_items = []
    with transaction.atomic():
        for raw_item in items:
            if not isinstance(raw_item, dict):
                raise ValidationError("审核项格式无效")

            content_type = str(raw_item.get("type") or "").strip()
            content_id = raw_item.get("id")
            if not content_type or not content_id:
                raise ValidationError("审核项缺少类型或 ID")

            processed_items.append(
                process_approval_item(
                    content_type=content_type,
                    content_id=int(content_id),
                    action=action,
                    actor=actor,
                    note=note,
                )
            )
    return processed_items


def _process_discussion_approval(content_id: int, action: str, actor, note: str) -> dict:
    if action not in {"approve", "reject"}:
        raise ValidationError("无效的审核动作")
    return process_runtime_discussion_approval_item(
        content_id=content_id,
        action=action,
        actor=actor,
        note=note,
    )


def _process_post_approval(content_id: int, action: str, actor, note: str) -> dict:
    if action not in {"approve", "reject"}:
        raise ValidationError("无效的审核动作")
    return process_runtime_post_approval_item(
        content_id=content_id,
        action=action,
        actor=actor,
        note=note,
    )

