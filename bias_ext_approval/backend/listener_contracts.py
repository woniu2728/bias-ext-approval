from __future__ import annotations

from bias_core.extensions import ExtensionEventListenerDefinition

from bias_ext_approval.backend.listeners import (
    handle_discussion_approved,
    handle_discussion_rejected,
    handle_discussion_resubmitted,
    handle_post_approved,
    handle_post_rejected,
    handle_post_resubmitted,
)


def approval_event_listener_definitions():
    return (
        ExtensionEventListenerDefinition(
            event_type="discussions.discussion.approved",
            handler=handle_discussion_approved,
            description="讨论审核通过后通知作者并写入讨论时间线。",
        ),
        ExtensionEventListenerDefinition(
            event_type="discussions.discussion.rejected",
            handler=handle_discussion_rejected,
            description="讨论审核拒绝后通知作者并写入讨论时间线。",
        ),
        ExtensionEventListenerDefinition(
            event_type="discussions.discussion.resubmitted",
            handler=handle_discussion_resubmitted,
            description="讨论重新提交审核后写入讨论时间线。",
        ),
        ExtensionEventListenerDefinition(
            event_type="posts.post.approved",
            handler=handle_post_approved,
            description="回复审核通过后通知作者并写入讨论时间线。",
        ),
        ExtensionEventListenerDefinition(
            event_type="posts.post.rejected",
            handler=handle_post_rejected,
            description="回复审核拒绝后通知作者并写入讨论时间线。",
        ),
        ExtensionEventListenerDefinition(
            event_type="posts.post.resubmitted",
            handler=handle_post_resubmitted,
            description="回复重新提交审核后写入讨论时间线。",
        ),
    )
