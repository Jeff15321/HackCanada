from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import AuthService, ProjectService

class SignupView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            print(f"Signup attempt for email: {email}")  # Debug log

            if not email or not password:
                print("Missing email or password in request")  # Debug log
                return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = AuthService.create_user(email, password)
            token = AuthService.generate_token(user['id'])
            
            print(f"Signup successful for user: {user['email']}")  # Debug log

            return Response({
                'token': token,
                'user': user
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            print(f"ValueError in SignupView: {str(e)}")  # Debug log
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Signup error: {str(e)}")  # Debug log
            import traceback
            print(f"Traceback: {traceback.format_exc()}")  # Debug log
            return Response({'error': f"Signup failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            print(f"Login attempt for email: {email}")  # Debug log

            if not email or not password:
                print("Missing email or password in request")  # Debug log
                return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = AuthService.authenticate_user(email, password)
            token = AuthService.generate_token(user['id'])
            
            print(f"Login successful for user: {user['email']}")  # Debug log

            return Response({
                'token': token,
                'user': user
            })

        except ValueError as e:
            print(f"ValueError in LoginView: {str(e)}")  # Debug log
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug log
            import traceback
            print(f"Traceback: {traceback.format_exc()}")  # Debug log
            return Response({'error': f"Login failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class AllUsersView(APIView):
    def get(self, request):
        try:
            users = AuthService.get_all_users()
            return Response({'users': users})

        except Exception as e:
            print(f"Get users error: {str(e)}")
            return Response(
                {'error': f"Failed to fetch users: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class NewProjectView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            project_name = request.data.get('project_name')
            collaborators = request.data.get('collaborators')
            is_public = request.data.get('is_public')

            project_id = ProjectService.create_project(
                user_id=user_id,
                project_name=project_name,
                collaborators=collaborators,
                is_public=is_public
            )

            return Response({'project_id': project_id}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"New project error: {str(e)}")
            return Response({'error': f"New project failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class AllProjectsView(APIView):
    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            print(f"Fetching projects for user_id: {user_id}")  # Debug log
            
            if not user_id:
                print("No user_id provided in request")  # Debug log
                return Response(
                    {'error': 'User ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            projects = ProjectService.get_user_projects(user_id)
            print(f"Found {len(projects)} projects")  # Debug log
            return Response({'projects': projects})

        except ValueError as e:
            print(f"ValueError in AllProjectsView: {str(e)}")  # Debug log
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Error in AllProjectsView: {str(e)}")  # Debug log
            import traceback
            print(f"Traceback: {traceback.format_exc()}")  # Debug log
            return Response(
                {'error': f"Failed to fetch projects: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteProjectView(APIView):
    def delete(self, request):
        try:
            project_id = request.query_params.get('project_id')
            ProjectService.delete_project(project_id)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Delete project error: {str(e)}")
            return Response(
                {'error': f"Failed to delete project: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# class OpenWhiteBoardView(APIView):
#     def post(self, request, project_id):
#         try:
#             user_id = request.data.get('user_id')
#             if not project_id or not user_id:
#                 return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

#             client = MongoClient(settings.MONGODB_URI)
#             db = client.get_database('projects')
#             projects_collection = db.projects

#             project = projects_collection.find_one({'_id': ObjectId(project_id)})
           
#             if not project:
#                 return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
            
#             # Check if user has permission
#             permissions = (
#                 user_id in [collaborator['id'] for collaborator in project.get('collaborators', [])] or 
#                 user_id == project.get('user_id') or 
#                 project.get('is_public', False)
#             )

#             if not permissions:
#                 return Response({'error': 'No permission to access this project'}, status=status.HTTP_403_FORBIDDEN)
            
#             project_client_data = {
#                 'id': str(project['_id']),
#                 'name': project['project_name'],
#                 'created_at': project['created_at'].isoformat(),
#                 'is_public': project.get('is_public', False),
#                 'collaborators': project.get('collaborators', []),
#                 'nodes': project.get('nodes', []),
#                 'connections': project.get('connections', [])
#             }
#             return Response({'project': project_client_data, 'permissions': permissions})

#         except Exception as e:
#             print(f"Error in OpenWhiteBoardView: {str(e)}")
#             return Response(
#                 {'error': f"Failed to open whiteboard: {str(e)}"}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

# class UploadWhiteBoardView(APIView):
#     def post(self, request):
#         try:
#             client = MongoClient(settings.MONGODB_URI)
#             db = client.get_database('projects')
#             projects_collection = db.projects

#             project = request.data.get('project')
#             user_id = request.data.get('user_id')
            
#             if not project or not user_id:
#                 return Response({'error': 'Project and user ID are required'}, status=status.HTTP_400_BAD_REQUEST)

#             # Convert project data to MongoDB format
#             project_data = {
#                 'project_name': project['name'],
#                 'is_public': project.get('is_public', False),
#                 'collaborators': project.get('collaborators', []),
#                 'nodes': project.get('nodes', []),
#                 'connections': project.get('connections', []),
#                 'user_id': user_id,
#                 'updated_at': datetime.now()
#             }
            
#             # Update the project in MongoDB
#             result = projects_collection.update_one(
#                 {'_id': ObjectId(project['id'])}, 
#                 {'$set': project_data}
#             )

#             if result.modified_count == 0:
#                 return Response({'error': 'Project not found or no changes made'}, status=status.HTTP_404_NOT_FOUND)

#             return Response({'message': 'Project saved successfully'}, status=status.HTTP_200_OK)

#         except Exception as e:
#             print(f"Error in UploadWhiteBoardView: {str(e)}")
#             return Response(
#                 {'error': f"Failed to save project: {str(e)}"}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
