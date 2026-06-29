from __future__ import annotations

from bias_core.extensions import PostTypeDefinition

from bias_ext_approval.backend.constants import EXTENSION_ID


def post_type_definitions():
    return (
        PostTypeDefinition(
            code="discussionApproved",
            label="讨论审核通过",
            module_id=EXTENSION_ID,
            description="记录讨论被管理员审核通过的系统事件帖，不计入回复统计和全文搜索。",
            icon="fas fa-check-circle",
            is_default=False,
            is_stream_visible=True,
            counts_toward_discussion=False,
            counts_toward_user=False,
            searchable=False,
        ),
        PostTypeDefinition(
            code="discussionRejected",
            label="讨论审核拒绝",
            module_id=EXTENSION_ID,
            description="记录讨论被管理员审核拒绝的系统事件帖，不计入回复统计和全文搜索。",
            icon="fas fa-ban",
            is_default=False,
            is_stream_visible=True,
            counts_toward_discussion=False,
            counts_toward_user=False,
            searchable=False,
        ),
        PostTypeDefinition(
            code="discussionResubmitted",
            label="讨论重新提交审核",
            module_id=EXTENSION_ID,
            description="记录作者修改被拒讨论后重新提交审核的系统事件帖，不计入回复统计和全文搜索。",
            icon="fas fa-rotate-right",
            is_default=False,
            is_stream_visible=True,
            counts_toward_discussion=False,
            counts_toward_user=False,
            searchable=False,
        ),
        PostTypeDefinition(
            code="postApproved",
            label="回复审核通过",
            module_id=EXTENSION_ID,
            description="记录回复被管理员审核通过的系统事件帖，不计入回复统计和全文搜索。",
            icon="fas fa-check",
            is_default=False,
            is_stream_visible=True,
            counts_toward_discussion=False,
            counts_toward_user=False,
            searchable=False,
        ),
        PostTypeDefinition(
            code="postRejected",
            label="回复审核拒绝",
            module_id=EXTENSION_ID,
            description="记录回复被管理员审核拒绝的系统事件帖，不计入回复统计和全文搜索。",
            icon="fas fa-comment-slash",
            is_default=False,
            is_stream_visible=True,
            counts_toward_discussion=False,
            counts_toward_user=False,
            searchable=False,
        ),
        PostTypeDefinition(
            code="postResubmitted",
            label="回复重新提交审核",
            module_id=EXTENSION_ID,
            description="记录作者修改被拒回复后重新提交审核的系统事件帖，不计入回复统计和全文搜索。",
            icon="fas fa-reply",
            is_default=False,
            is_stream_visible=True,
            counts_toward_discussion=False,
            counts_toward_user=False,
            searchable=False,
        ),
    )
