from datetime import datetime

class ProjectService:
    @staticmethod
    async def get_user_projects(user_id: str):
        """
        Get all projects for a user
        For now, returns dummy data
        """
        return [
            {
                "id": "1",
                "name": "Test Project 1",
                "created_at": datetime.utcnow(),
                "is_public": True,
                "collaborators": []
            },
            {
                "id": "2",
                "name": "Test Project 2",
                "created_at": datetime.utcnow(),
                "is_public": False,
                "collaborators": []
            }
        ] 