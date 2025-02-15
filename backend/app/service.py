from django.conf import settings
import jwt
from datetime import datetime, timedelta
from bcrypt import hashpw, gensalt
from pymongo import MongoClient
from bson.objectid import ObjectId

class AuthService:
    @staticmethod
    def get_db():
        client = MongoClient(settings.MONGODB_URI)
        return client.get_database('users')

    @staticmethod
    def create_user(email: str, password: str):
        db = AuthService.get_db()
        users_collection = db.users

        if users_collection.find_one({'email': email}):
            raise ValueError('User with this email already exists')

        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        mongo_user = users_collection.insert_one({
            'email': email,
            'password': hashed_password,
            'created_at': datetime.now()
        })

        return {
            'email': email,
            'id': str(mongo_user.inserted_id)
        }

    @staticmethod
    def authenticate_user(email: str, password: str):
        db = AuthService.get_db()
        users_collection = db.users

        user_data = users_collection.find_one({'email': email})
        if not user_data:
            raise ValueError('User not found')

        if not hashpw(password.encode('utf-8'), user_data['password']) == user_data['password']:
            raise ValueError('Invalid password')

        return {
            'email': user_data['email'],
            'id': str(user_data['_id'])
        }

    @staticmethod
    def generate_token(user_id: str):
        return jwt.encode(
            {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(days=1)},
            'your_secret_key',
            algorithm='HS256'
        )

    @staticmethod
    def get_all_users():
        db = AuthService.get_db()
        users_collection = db.users
        users = users_collection.find({}, {'email': 1})
        return [{'email': user['email'], 'id': str(user['_id'])} for user in users]

class ProjectService:
    @staticmethod
    def get_db():
        client = MongoClient(**settings.MONGODB_SETTINGS)
        return client.get_database('projects')

    @staticmethod
    def create_project(user_id: str, project_name: str, collaborators=None, is_public=False):
        if not user_id or not project_name:
            raise ValueError('User ID and project name are required')

        db = ProjectService.get_db()
        projects_collection = db.projects

        project_id = projects_collection.insert_one({
            'user_id': user_id,
            'project_name': project_name,
            'created_at': datetime.now(),
            'nodes': [],
            'connections': [],
            'collaborators': collaborators or [],
            'is_public': is_public
        })

        return str(project_id.inserted_id)

    @staticmethod
    def get_user_projects(user_id: str):
        if not user_id:
            raise ValueError('User ID is required')

        db = ProjectService.get_db()
        projects_collection = db.projects

        projects = list(projects_collection.find({'user_id': user_id}))
        return [{
            'id': str(project['_id']),
            'name': project['project_name'],
            'created_at': project['created_at'].isoformat(),
            'is_public': project.get('is_public', False),
            'collaborators': project.get('collaborators', [])
        } for project in projects]

    @staticmethod
    def delete_project(project_id: str):
        if not project_id:
            raise ValueError('Project ID is required')

        db = ProjectService.get_db()
        projects_collection = db.projects

        result = projects_collection.delete_one({'_id': ObjectId(project_id)})
        if result.deleted_count != 1:
            raise ValueError('Project not found')
