from __future__ import annotations

from bias_core.extensions import AdminPageDefinition, PermissionDefinition

from bias_ext_approval.backend.constants import EXTENSION_ID


def permission_definitions():
    return (
        PermissionDefinition(
            code="admin.approval.view",
            label="查看审核队列",
            section="moderation",
            section_label="审核与举报",
            module_id=EXTENSION_ID,
            icon="fas fa-user-check",
            description="允许在后台查看待审核讨论与回复队列。",
        ),
        PermissionDefinition(
            code="admin.approval.approve",
            label="通过审核内容",
            section="moderation",
            section_label="审核与举报",
            module_id=EXTENSION_ID,
            icon="fas fa-check-circle",
            description="允许在后台通过待审核讨论与回复。",
            required_permissions=("admin.approval.view",),
        ),
        PermissionDefinition(
            code="admin.approval.reject",
            label="拒绝审核内容",
            section="moderation",
            section_label="审核与举报",
            module_id=EXTENSION_ID,
            icon="fas fa-ban",
            description="允许在后台拒绝待审核讨论与回复并填写审核反馈。",
            required_permissions=("admin.approval.view",),
        ),
    )


def admin_page_definitions():
    return (
        AdminPageDefinition(
            path="/admin/approval",
            label="审核队列",
            icon="fas fa-user-check",
            module_id=EXTENSION_ID,
            nav_section="feature",
            description="处理待审核讨论与回复。",
        ),
    )
