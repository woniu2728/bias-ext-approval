from bias_ext_approval.backend.extenders import (
    admin_extenders,
    event_extenders,
    forum_extenders,
    frontend_extenders,
    optional_integration_extenders,
    resource_extenders,
    service_extenders,
)


def extend():
    return [
        *frontend_extenders(),
        *admin_extenders(),
        *service_extenders(),
        *resource_extenders(),
        *forum_extenders(),
        *event_extenders(),
        *optional_integration_extenders(),
    ]
