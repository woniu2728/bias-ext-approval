from __future__ import annotations

from bias_core.extensions import NotificationsExtender


def notification_extender():
    return (
        NotificationsExtender()
        .type(
            "discussionApproved",
            label="讨论审核通过",
            description="通知作者其讨论已通过审核。",
            icon="fas fa-circle-check",
            navigation_scope="discussion",
            preference_key="notify_discussion_approval",
            preference_label="讨论审核结果通知",
            preference_description="当你的讨论被审核通过或拒绝时通知你。",
        )
        .type(
            "discussionRejected",
            label="讨论审核拒绝",
            description="通知作者其讨论未通过审核。",
            icon="fas fa-circle-xmark",
            navigation_scope="discussion",
            preference_key="notify_discussion_approval",
            preference_label="讨论审核结果通知",
            preference_description="当你的讨论被审核通过或拒绝时通知你。",
        )
        .type(
            "postApproved",
            label="回复审核通过",
            description="通知作者其回复已通过审核。",
            icon="fas fa-check",
            navigation_scope="post",
            preference_key="notify_post_approval",
            preference_label="回复审核结果通知",
            preference_description="当你的回复被审核通过或拒绝时通知你。",
        )
        .type(
            "postRejected",
            label="回复审核拒绝",
            description="通知作者其回复未通过审核。",
            icon="fas fa-xmark",
            navigation_scope="post",
            preference_key="notify_post_approval",
            preference_label="回复审核结果通知",
            preference_description="当你的回复被审核通过或拒绝时通知你。",
        )
    )
