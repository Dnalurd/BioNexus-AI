"""Database models for BioNexus AI."""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum, Float, Integer, String, Text, UniqueConstraint, Index, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class Organization(Base):
    """Organization model for multi-tenant support."""

    __tablename__ = "organizations"
    __table_args__ = (Index("ix_org_code", "code"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users: Mapped[list["User"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    patients: Mapped[list["Patient"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    laboratories: Mapped[list["Laboratory"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    tests: Mapped[list["Test"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    samples: Mapped[list["Sample"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    results: Mapped[list["Result"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    inventory_items: Mapped[list["InventoryItem"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    equipment: Mapped[list["Equipment"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="organization", cascade="all, delete-orphan")


class User(Base):
    """User model with role-based access control."""

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", "organization_id", name="uq_user_email_org"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    role: Mapped[str] = mapped_column(String(50), default="viewer")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped[Organization] = relationship(back_populates="users")
    permissions: Mapped[list["Permission"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Permission(Base):
    """User permissions model."""

    __tablename__ = "permissions"
    __table_args__ = (UniqueConstraint("user_id", "permission_code", name="uq_user_perm"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    permission_code: Mapped[str] = mapped_column(String(100))
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user: Mapped[User] = relationship(back_populates="permissions")


class Patient(Base):
    """Patient model with medical record management."""

    __tablename__ = "patients"
    __table_args__ = (UniqueConstraint("medical_record_number", "organization_id", name="uq_patient_mrn_org"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    medical_record_number: Mapped[str] = mapped_column(String(50), index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    gender: Mapped[str] = mapped_column(String(10))  # M, F, O
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    address: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(String(100))
    country: Mapped[Optional[str]] = mapped_column(String(100))
    blood_type: Mapped[Optional[str]] = mapped_column(String(5))
    allergies: Mapped[Optional[str]] = mapped_column(Text)
    medical_history: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped[Organization] = relationship(back_populates="patients")
    samples: Mapped[list["Sample"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    lab_requests: Mapped[list["LabRequest"]] = relationship(back_populates="patient", cascade="all, delete-orphan")


class Laboratory(Base):
    """Laboratory model."""

    __tablename__ = "laboratories"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255))
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    accreditation: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped[Organization] = relationship(back_populates="laboratories")
    tests: Mapped[list["Test"]] = relationship(back_populates="laboratory", cascade="all, delete-orphan")


class Test(Base):
    """Test/Analysis model."""

    __tablename__ = "tests"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    laboratory_id: Mapped[UUID] = mapped_column(ForeignKey("laboratories.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(Text)
    sample_type: Mapped[str] = mapped_column(String(100))
    turnaround_time_hours: Mapped[int] = mapped_column(Integer)
    reference_range: Mapped[Optional[str]] = mapped_column(String(255))
    unit: Mapped[Optional[str]] = mapped_column(String(50))
    normal_min: Mapped[Optional[Float]] = mapped_column(Float)
    normal_max: Mapped[Optional[Float]] = mapped_column(Float)
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False)
    critical_min: Mapped[Optional[Float]] = mapped_column(Float)
    critical_max: Mapped[Optional[Float]] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped[Organization] = relationship(back_populates="tests")
    laboratory: Mapped[Laboratory] = relationship(back_populates="tests")
    results: Mapped[list["Result"]] = relationship(back_populates="test", cascade="all, delete-orphan")
    lab_request_tests: Mapped[list["LabRequestTest"]] = relationship(back_populates="test", cascade="all, delete-orphan")


class LabRequest(Base):
    """Laboratory request model."""

    __tablename__ = "lab_requests"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    patient_id: Mapped[UUID] = mapped_column(ForeignKey("patients.id"), nullable=False)
    request_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    priority: Mapped[str] = mapped_column(String(20), default="routine")  # routine, urgent, stat
    clinical_indication: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    requested_by: Mapped[str] = mapped_column(String(255))
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    approved_by: Mapped[Optional[str]] = mapped_column(String(255))
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped[Organization] = relationship(back_populates="results")  # Note: should be lab_requests
    patient: Mapped[Patient] = relationship(back_populates="lab_requests")
    tests: Mapped[list["LabRequestTest"]] = relationship(back_populates="lab_request", cascade="all, delete-orphan")
    samples: Mapped[list["Sample"]] = relationship(back_populates="lab_request", cascade="all, delete-orphan")


class LabRequestTest(Base):
    """Junction table for lab requests and tests (many-to-many)."""

    __tablename__ = "lab_request_tests"
    __table_args__ = (UniqueConstraint("lab_request_id", "test_id", name="uq_req_test"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    lab_request_id: Mapped[UUID] = mapped_column(ForeignKey("lab_requests.id"), nullable=False)
    test_id: Mapped[UUID] = mapped_column(ForeignKey("tests.id"), nullable=False)

    # Relationships
    lab_request: Mapped[LabRequest] = relationship(back_populates="tests")
    test: Mapped[Test] = relationship(back_populates="lab_request_tests")


class Sample(Base):
    """Sample/Specimen model with tracking."""

    __tablename__ = "samples"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    patient_id: Mapped[UUID] = mapped_column(ForeignKey("patients.id"), nullable=False)
    lab_request_id: Mapped[UUID] = mapped_column(ForeignKey("lab_requests.id"), nullable=False)
    sample_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    barcode: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True)
    qr_code: Mapped[Optional[str]] = mapped_column(String(500))
    sample_type: Mapped[str] = mapped_column(String(100))
    collection_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    collection_location: Mapped[Optional[str]] = mapped_column(String(255))
    collected_by: Mapped[str] = mapped_column(String(255))
    volume: Mapped[Optional[Float]] = mapped_column(Float)
    volume_unit: Mapped[Optional[str]] = mapped_column(String(10))  # mL, µL
    status: Mapped[str] = mapped_column(String(50), default="registered")
    reception_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    received_by: Mapped[Optional[str]] = mapped_column(String(255))
    processing_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    quality_issue: Mapped[Optional[str]] = mapped_column(Text)
    rejected_reason: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped[Organization] = relationship(back_populates="samples")
    patient: Mapped[Patient] = relationship(back_populates="samples")
    lab_request: Mapped[LabRequest] = relationship(back_populates="samples")
    results: Mapped[list["Result"]] = relationship(back_populates="sample", cascade="all, delete-orphan")
    tracking_events: Mapped[list["SampleTracking"]] = relationship(back_populates="sample", cascade="all, delete-orphan")


class SampleTracking(Base):
    """Sample tracking for chain of custody."""

    __tablename__ = "sample_tracking"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    sample_id: Mapped[UUID] = mapped_column(ForeignKey("samples.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50))
    location: Mapped[Optional[str]] = mapped_column(String(255))
    handled_by: Mapped[str] = mapped_column(String(255))
    event_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    sample: Mapped[Sample] = relationship(back_populates="tracking_events")


class Result(Base):
    """Test result model."""

    __tablename__ = "results"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    sample_id: Mapped[UUID] = mapped_column(ForeignKey("samples.id"), nullable=False)
    test_id: Mapped[UUID] = mapped_column(ForeignKey("tests.id"), nullable=False)
    result_value: Mapped[Optional[str]] = mapped_column(String(500))
    result_numeric: Mapped[Optional[Float]] = mapped_column(Float)
    unit: Mapped[Optional[str]] = mapped_column(String(50))
    reference_range: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    is_critical: Mapped[bool] = mapped_column(Boolean, default=False)
    critical_alert_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    entered_by: Mapped[Optional[str]] = mapped_column(String(255))
    entered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    verified_by: Mapped[Optional[str]] = mapped_column(String(255))
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    approved_by: Mapped[Optional[str]] = mapped_column(String(255))
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    released_by: Mapped[Optional[str]] = mapped_column(String(255))
    released_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    comments: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped[Organization] = relationship(back_populates="results")
    sample: Mapped[Sample] = relationship(back_populates="results")
    test: Mapped[Test] = relationship(back_populates="results")


class InventoryItem(Base):
    """Inventory model for reagents and consumables."""

    __tablename__ = "inventory_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(100), index=True)
    name: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(100))
    supplier: Mapped[Optional[str]] = mapped_column(String(255))
    batch_number: Mapped[Optional[str]] = mapped_column(String(100))
    quantity_on_hand: Mapped[int] = mapped_column(Integer, default=0)
    unit: Mapped[str] = mapped_column(String(50))
    reorder_level: Mapped[int] = mapped_column(Integer)
    reorder_quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[Optional[Float]] = mapped_column(Float)
    expiry_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    storage_location: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped[Organization] = relationship(back_populates="inventory_items")


class Equipment(Base):
    """Equipment model with maintenance tracking."""

    __tablename__ = "equipment"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    model: Mapped[Optional[str]] = mapped_column(String(255))
    manufacturer: Mapped[Optional[str]] = mapped_column(String(255))
    serial_number: Mapped[Optional[str]] = mapped_column(String(100))
    installation_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(50), default="operational")
    location: Mapped[Optional[str]] = mapped_column(String(255))
    last_calibration_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    next_calibration_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_maintenance_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    next_maintenance_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped[Organization] = relationship(back_populates="equipment")


class AuditLog(Base):
    """Audit log for tracking all user actions."""

    __tablename__ = "audit_logs"
    __table_args__ = (Index("ix_audit_user_action", "user_id", "action"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(100))
    resource_type: Mapped[str] = mapped_column(String(100))
    resource_id: Mapped[Optional[UUID]] = mapped_column()
    old_values: Mapped[Optional[dict]] = mapped_column(JSON)
    new_values: Mapped[Optional[dict]] = mapped_column(JSON)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50))
    user_agent: Mapped[Optional[str]] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50))  # success, failure
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)

    # Relationships
    organization: Mapped[Organization] = relationship(back_populates="audit_logs")
    user: Mapped[Optional[User]] = relationship(back_populates="audit_logs")
