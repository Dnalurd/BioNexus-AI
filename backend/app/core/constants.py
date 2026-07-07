"""Application constants."""

# User Roles
class UserRole:
    ADMIN = "admin"
    LABORATORY_DIRECTOR = "laboratory_director"
    LABORATORY_MANAGER = "laboratory_manager"
    TECHNICIAN = "technician"
    ANALYST = "analyst"
    PHLEBOTOMIST = "phlebotomist"
    CLINICIAN = "clinician"
    RESEARCHER = "researcher"
    QUALITY_OFFICER = "quality_officer"
    VIEWER = "viewer"

    ALL = [
        ADMIN,
        LABORATORY_DIRECTOR,
        LABORATORY_MANAGER,
        TECHNICIAN,
        ANALYST,
        PHLEBOTOMIST,
        CLINICIAN,
        RESEARCHER,
        QUALITY_OFFICER,
        VIEWER,
    ]


# Permissions
class Permission:
    # User Management
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_MANAGE_ROLES = "user:manage_roles"

    # Patient Management
    PATIENT_CREATE = "patient:create"
    PATIENT_READ = "patient:read"
    PATIENT_UPDATE = "patient:update"
    PATIENT_DELETE = "patient:delete"
    PATIENT_EXPORT = "patient:export"

    # Laboratory
    LAB_REQUEST_CREATE = "lab:request_create"
    LAB_REQUEST_READ = "lab:request_read"
    LAB_REQUEST_UPDATE = "lab:request_update"
    LAB_REQUEST_APPROVE = "lab:request_approve"
    LAB_RESULT_ENTER = "lab:result_enter"
    LAB_RESULT_VERIFY = "lab:result_verify"
    LAB_RESULT_RELEASE = "lab:result_release"

    # Inventory
    INVENTORY_READ = "inventory:read"
    INVENTORY_UPDATE = "inventory:update"
    INVENTORY_MANAGE = "inventory:manage"

    # Equipment
    EQUIPMENT_READ = "equipment:read"
    EQUIPMENT_UPDATE = "equipment:update"
    EQUIPMENT_MANAGE = "equipment:manage"

    # Quality
    QUALITY_READ = "quality:read"
    QUALITY_UPDATE = "quality:update"
    QUALITY_MANAGE = "quality:manage"

    # Reports
    REPORT_READ = "report:read"
    REPORT_GENERATE = "report:generate"
    REPORT_EXPORT = "report:export"

    # AI/Analytics
    AI_READ = "ai:read"
    ANALYTICS_READ = "analytics:read"

    # System
    SYSTEM_ADMIN = "system:admin"
    AUDIT_READ = "audit:read"


# Sample Status
class SampleStatus:
    REGISTERED = "registered"
    COLLECTED = "collected"
    IN_TRANSIT = "in_transit"
    RECEIVED = "received"
    PROCESSING = "processing"
    COMPLETED = "completed"
    REJECTED = "rejected"
    LOST = "lost"

    ALL = [
        REGISTERED,
        COLLECTED,
        IN_TRANSIT,
        RECEIVED,
        PROCESSING,
        COMPLETED,
        REJECTED,
        LOST,
    ]


# Result Status
class ResultStatus:
    PENDING = "pending"
    ENTERED = "entered"
    VERIFIED = "verified"
    APPROVED = "approved"
    RELEASED = "released"
    CANCELLED = "cancelled"

    ALL = [PENDING, ENTERED, VERIFIED, APPROVED, RELEASED, CANCELLED]


# Test Category
class TestCategory:
    HEMATOLOGY = "hematology"
    CHEMISTRY = "chemistry"
    IMMUNOLOGY = "immunology"
    MICROBIOLOGY = "microbiology"
    VIROLOGY = "virology"
    SEROLOGY = "serology"
    URINALYSIS = "urinalysis"
    COAGULATION = "coagulation"
    TOXICOLOGY = "toxicology"
    GENETICS = "genetics"

    ALL = [
        HEMATOLOGY,
        CHEMISTRY,
        IMMUNOLOGY,
        MICROBIOLOGY,
        VIROLOGY,
        SEROLOGY,
        URINALYSIS,
        COAGULATION,
        TOXICOLOGY,
        GENETICS,
    ]


# Quality Check Status
class QCStatus:
    PASSED = "passed"
    FAILED = "failed"
    PENDING = "pending"
    NOT_APPLICABLE = "not_applicable"

    ALL = [PASSED, FAILED, PENDING, NOT_APPLICABLE]


# Equipment Status
class EquipmentStatus:
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    CALIBRATION = "calibration"
    BREAKDOWN = "breakdown"
    DECOMMISSIONED = "decommissioned"

    ALL = [OPERATIONAL, MAINTENANCE, CALIBRATION, BREAKDOWN, DECOMMISSIONED]


# Audit Action
class AuditAction:
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    RELEASE = "release"
    LOGIN = "login"
    LOGOUT = "logout"
    PERMISSION_GRANT = "permission_grant"
    PERMISSION_REVOKE = "permission_revoke"
