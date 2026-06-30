from __future__ import annotations

from bias_core.extensions import (
    AdminSurfaceExtender,
    ApiResourceExtender,
    ApiRoutesExtender,
    ConditionalExtender,
    EventListenersExtender,
    ForumCapabilitiesExtender,
    LifecycleExtender,
    PostEventExtender,
    RuntimeServiceContractExtender,
    ServiceProviderExtender,
)

from bias_ext_approval.backend.admin_api import router as approval_admin_router
from bias_ext_approval.backend.admin_surface import admin_page_definitions, permission_definitions
from bias_ext_approval.backend.forum_contracts import post_type_definitions
from bias_ext_approval.backend.frontend import frontend_extender
from bias_ext_approval.backend.listener_contracts import approval_event_listener_definitions
from bias_ext_approval.backend.notification_contracts import notification_extender
from bias_ext_approval.backend.realtime_contracts import realtime_extender
from bias_ext_approval.backend.resources import (
    APPROVAL_POST_EVENT_TYPES,
    admin_stats_resource_field_definitions,
    resolve_approval_event_data,
)
from bias_ext_approval.backend.runtime import approval_service_provider


def frontend_extenders():
    return (frontend_extender(),)


def admin_extenders():
    return (
        AdminSurfaceExtender(
            permissions=permission_definitions(),
            admin_pages=admin_page_definitions(),
            permissions_pages=("/admin/extensions/approval/permissions",),
            operations_pages=("/admin/extensions/approval/operations",),
        ),
        ApiRoutesExtender(
            mounts=(("/admin", approval_admin_router),),
            tags=("Admin",),
        ),
    )


def resource_extenders():
    return (
        ApiResourceExtender("admin_stats").fields(admin_stats_resource_field_definitions),
    )


def forum_extenders():
    return (
        ForumCapabilitiesExtender(
            post_types=post_type_definitions(),
        ),
        PostEventExtender().types(
            APPROVAL_POST_EVENT_TYPES,
            resolve_approval_event_data,
            description="审核系统事件帖的结构化 payload。",
        ),
    )


def event_extenders():
    return (
        EventListenersExtender(
            listeners=approval_event_listener_definitions(),
        ),
        realtime_extender(),
    )


def notification_integration_extenders():
    return (
        notification_extender(),
    )


def optional_integration_extenders():
    return (
        ConditionalExtender().when_extension_enabled("notifications", notification_integration_extenders),
    )


def service_extenders():
    return (
        ServiceProviderExtender(
            key="approval.service",
            provider=approval_service_provider,
        ),
        RuntimeServiceContractExtender().service(
            "approval.service",
            required_methods=(
                "bulk_process",
                "list_queue",
                "process_item",
                "serialize_item",
            ),
        ),
        LifecycleExtender(),
    )
