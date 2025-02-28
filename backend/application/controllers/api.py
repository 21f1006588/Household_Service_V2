from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse, fields, marshal_with, Api
from application.data.model import User as user_model, Role, db
import datetime
from flask_security import auth_required, current_user, hash_password, SQLAlchemyUserDatastore, Security
import os
from flask_caching import Cache

cache = Cache()
wrkng_dir = os.path.abspath(os.path.dirname(__file__))

user_datastore = SQLAlchemyUserDatastore(db, user_model, Role)
security = Security(user_datastore)

# Extend the request parser to include a user_type field.
user_req_args = reqparse.RequestParser()
user_req_args.add_argument('name', help="Name of the user")
user_req_args.add_argument('username', required=True, help="Username required")
user_req_args.add_argument('email', required=True, help="Email required")
user_req_args.add_argument('password', required=True, help="Password required")
user_req_args.add_argument('user_type', required=True, help="User type required: 'customer' or 'service professional'")

# Updated fields to return key user attributes (including admin-related flags).
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'username': fields.String,
    'email': fields.String,
    'date_created': fields.DateTime(dt_format='iso8601'),
    'user_type': fields.String,
    'approved': fields.Boolean,
    'is_blocked': fields.Boolean
}

class UserAPI(Resource):
    @auth_required('token')
    @cache.memoize(5)
    def get(self, email):
        u = user_model.query.filter_by(email=email).first()
        if not u:
            return jsonify({"error": "User not found"}), 404

        user_details = {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "name": u.name,
            "date_created": u.date_created.isoformat() if u.date_created else None,
            "phone_number": u.phone_number,
            "service_type": u.service_type,
            "experience": u.experience,
            "location": u.location,
            "pincode": u.pincode,
            "approved": u.approved,
            "is_blocked": u.is_blocked,
            "user_type": u.user_type
        }
        return jsonify(user_details)

    @auth_required('token')
    def put(self, email):
        u = user_model.query.filter_by(email=email).first()
        if not u:
            return jsonify({"error": "User not found"}), 404

        # Update fields that any user can update.
        new_email = request.form.get('email')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        service_type = request.form.get('service_type')
        experience = request.form.get('experience')
        location = request.form.get('location')
        pincode = request.form.get('pincode')

        if new_email:
            u.email = new_email
        if name:
            u.name = name
        if phone_number:
            u.phone_number = phone_number
        if service_type:
            u.service_type = service_type
        if experience:
            try:
                u.experience = int(experience)
            except ValueError:
                pass
        if location:
            u.location = location
        if pincode:
            u.pincode = pincode

        # Admin-only updates: block/unblock and approval status.
        # Only an admin (determined by their roles) can update these.
        if request.form.get('is_blocked') is not None:
            if any(role.name.lower() == "admin" for role in current_user.roles):
                u.is_blocked = request.form.get('is_blocked').lower() in ['true', '1', 'yes']
            else:
                return jsonify({"error": "Permission denied for updating block status"}), 403

        if request.form.get('approved') is not None:
            if any(role.name.lower() == "admin" for role in current_user.roles):
                u.approved = request.form.get('approved').lower() in ['true', '1', 'yes']
            else:
                return jsonify({"error": "Permission denied for updating approval status"}), 403

        db.session.commit()
        return jsonify({"message": "User Updated"})

    @marshal_with(user_fields)
    def post(self):
        args = user_req_args.parse_args()
        name = args.get("name")
        username = args.get("username")
        email = args.get("email")
        password = args.get("password")
        user_type = args.get("user_type").lower()

        # Only allow registration as a customer or service professional.
        if user_type not in ["customer", "service professional"]:
            return {'error': "Invalid user type. Only 'customer' or 'service professional' are allowed."}, 400

        # Disallow public registration as an admin.
        if user_type == "admin":
            return {'error': "Registration as admin is not allowed."}, 400

        # Check if email or username already exists.
        if user_model.query.filter_by(email=email).first():
            return {'error': 'Email already belongs to an account. Try another email.'}, 400
        if user_model.query.filter_by(username=username).first():
            return {'error': 'Username already belongs to an account. Try another username.'}, 400

        # Automatically approve customers; require admin approval for service professionals.
        approved = True if user_type == "customer" else False

        # Create the new user.
        user_datastore.create_user(
            email=email,
            name=name,
            username=username,
            password=hash_password(password),
            user_type=user_type,
            approved=approved
        )
        db.session.commit()

        u_data = user_model.query.filter_by(email=email).first()
        return {
            "id": u_data.id,
            "username": u_data.username,
            "email": u_data.email,
            "name": u_data.name,
            "date_created": u_data.date_created.isoformat() if u_data.date_created else None,
            "user_type": u_data.user_type,
            "approved": u_data.approved,
            "is_blocked": u_data.is_blocked
        }, 200

    @auth_required('token')
    def delete(self, email):
        u = user_model.query.filter_by(email=email).first()
        if not u:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(u)
        db.session.commit()
        return jsonify({"message": "User Deleted"})
