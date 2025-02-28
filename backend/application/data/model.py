import uuid
from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Role model for role-based authentication
class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

# Association table for linking users and roles
class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))

# Unified User table for all user types
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Required by Flask-Security
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    active = db.Column(db.Boolean(), default=True)
    
    # Common fields for all users
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed automatically by Flask-Security
    name = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_blocked = db.Column(db.Boolean, default=False)
    
    # Optional fields (for service professionals or customers)
    phone_number = db.Column(db.String(15), nullable=True)
    service_type = db.Column(db.String(50), nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)
    approved = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String(50), nullable=True)
    
    # Role-based relationship
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

# Service model referencing an admin user (who created the service)
class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)  # in minutes
    description = db.Column(db.Text)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    # Relationship to the admin (a user with admin role) who created the service
    admin = db.relationship('User', backref=db.backref('services', lazy='dynamic'))

# ServiceRequest model where both customer and professional are users
class ServiceRequest(db.Model):
    __tablename__ = "service_requests"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id', ondelete='CASCADE'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(20), nullable=False, default="requested")
    remarks = db.Column(db.Text, nullable=True)
    
    # Specify foreign keys to differentiate customer and professional relationships
    customer = db.relationship('User', foreign_keys=[customer_id],
                               backref=db.backref('customer_requests', lazy='dynamic'))
    professional = db.relationship('User', foreign_keys=[professional_id],
                                   backref=db.backref('professional_requests', lazy='dynamic'))
    service = db.relationship('Service', backref=db.backref('service_requests', lazy='dynamic'))
