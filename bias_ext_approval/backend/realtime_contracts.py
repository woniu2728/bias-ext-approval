from __future__ import annotations

from bias_core.extensions import RealtimeExtender


def realtime_extender():
    return (
        RealtimeExtender()
        .broadcast_discussion_event(
            "discussions.discussion.approved",
            "discussion.approved",
            include_discussion=True,
            include_post=True,
            post_id_getter=lambda current_discussion: current_discussion.first_post_id,
            description="讨论审核通过后向讨论实时流广播审核状态变更。",
        )
        .broadcast_discussion_event(
            "discussions.discussion.rejected",
            "discussion.rejected",
            description="讨论审核拒绝后向讨论实时流广播审核状态变更。",
        )
        .broadcast_discussion_event(
            "discussions.discussion.resubmitted",
            "discussion.resubmitted",
            description="讨论重新提交审核后向讨论实时流广播审核状态变更。",
        )
        .broadcast_discussion_event(
            "posts.post.approved",
            "post.approved",
            include_discussion=True,
            description="回复审核通过后向讨论实时流广播审核状态变更。",
        )
        .broadcast_discussion_event(
            "posts.post.rejected",
            "post.rejected",
            description="回复审核拒绝后向讨论实时流广播审核状态变更。",
        )
        .broadcast_discussion_event(
            "posts.post.resubmitted",
            "post.resubmitted",
            description="回复重新提交审核后向讨论实时流广播审核状态变更。",
        )
    )
