from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.shortcuts import get_object_or_404
from core.response import *
from .models import *
from .serializers import *
from django.db.models import Q
from apps.tracker.utils import notify_project


class ProjectCRUDView(APIView):
    """
    Handles CRUD operations for ProjectModel.
    
    Methods:
    - GET: Retrieve all projects or a specific project by ID.
    - POST: Create a new project.
    - PATCH: Partially update a project.
    - DELETE: Delete a project.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    queryset = ProjectModel.objects.all()

    def get(self, request):
        """
        Retrieve a specific project by ID (if provided),
        or return a list of all projects.
        """
        project_id = request.query_params.get("project_id")

        if project_id:
            # Try to fetch specific project by ID
            try:
                project = self.queryset.get(id=project_id)
                serializer = self.serializer_class(project)
                return CustomApiResponse(
                    status="success",
                    message="Project retrieved successfully.",
                    data=serializer.data,
                    code=status.HTTP_200_OK
                ).get_response()
            except ProjectModel.DoesNotExist:
                # If project not found, return custom 404 response
                return CustomApiResponse(
                    status="error",
                    message="Project not found.",
                    data={},
                    code=status.HTTP_404_NOT_FOUND
                ).get_response()
        else:
            # If no project_id is given, return all projects
            projects = self.queryset.all()
            serializer = self.serializer_class(projects, many=True)
            return CustomApiResponse(
                status="success",
                message="All projects retrieved successfully.",
                data=serializer.data,
                code=status.HTTP_200_OK
            ).get_response()
        

    def post(self, request):
        current_user = request.user
        data = request.data.copy()
        data["owner"] = current_user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return CustomApiResponse(
                status='success',
                message='Prject successful!',
                data=serializer.data,
                code=status.HTTP_201_CREATED
            ).get_response()
        
        return CustomApiResponse(
            status='error',
            message='Prject Create failed',
            data=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        ).get_response()

    def patch(self, request):
        """
        Partial update of a project.
        Requires 'project_id' query parameter.
        """
        project_id = request.query_params.get("project_id")
        if not project_id:
            return CustomApiResponse(
                status="error",
                message="Project ID is required for update.",
                data={},
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()

        try:
            project = self.queryset.get(id=project_id)
        except ProjectModel.DoesNotExist:
            return CustomApiResponse(
                status="error",
                message="Project not found.",
                data={},
                code=status.HTTP_404_NOT_FOUND
            ).get_response()

        serializer = self.serializer_class(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomApiResponse(
                status="success",
                message="Project updated successfully.",
                data=serializer.data,
                code=status.HTTP_200_OK
            ).get_response()

        return CustomApiResponse(
            status="error",
            message="Project update failed.",
            data=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        ).get_response()
    

    def delete(self, request):
        """
        Delete a project.
        Requires 'project_id' query parameter.
        """
        project_id = request.query_params.get("project_id")
        if not project_id:
            return CustomApiResponse(
                status="error",
                message="Project ID is required for deletion.",
                data={},
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()

        try:
            project = self.queryset.get(id=project_id)
            project.delete()
            return CustomApiResponse(
                status="success",
                message="Project deleted successfully.",
                data={},
                code=status.HTTP_204_NO_CONTENT
            ).get_response()
        except ProjectModel.DoesNotExist:
            return CustomApiResponse(
                status="error",
                message="Project not found.",
                data={},
                code=status.HTTP_404_NOT_FOUND
            ).get_response()


class BugCRUDView(APIView):
    """
    Handles CRUD operations for BugModel.
    
    Methods:
    - GET: Retrieve all Bug or a specific Bug by ID.
    - POST: Create a new Bug.
    - PATCH: Partially update a Bug.
    - DELETE: Delete a Bug.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BugSerializer
    queryset = BugModel.objects.all()

    def get(self, request):
        """
        Retrieve a specific Bug by ID (if provided),
        or return a list of all BugModel.
        """
        bug_id = request.query_params.get("bug_id")
        project_id = request.query_params.get("project_id")
        bug_status = request.query_params.get("status")
        q_project = Q(project=project_id) if project_id else Q()
        q_bug_status = Q(status=bug_status) if bug_status else Q()


        if bug_id:
            # Try to fetch specific bug by ID
            try:
                bug = self.queryset.get(id=bug_id)
                serializer = self.serializer_class(bug)
                return CustomApiResponse(
                    status="success",
                    message="Bug retrieved successfully.",
                    data=serializer.data,
                    code=status.HTTP_200_OK
                ).get_response()
            except BugModel.DoesNotExist:
                # If bug not found, return custom 404 response
                return CustomApiResponse(
                    status="error",
                    message="Bug not found.",
                    data={},
                    code=status.HTTP_404_NOT_FOUND
                ).get_response()
        else:
            # If no bug_id is given, return all bug and also Supports filtering by project_id, status, 
            bugs = self.queryset.filter(q_project,q_bug_status)
            serializer = self.serializer_class(bugs, many=True)
            return CustomApiResponse(
                status="success",
                message="All bug retrieved successfully.",
                data=serializer.data,
                code=status.HTTP_200_OK
            ).get_response()
        

    def post(self, request):
        current_user = request.user
        data = request.data.copy()
        data["created_by"] = current_user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return CustomApiResponse(
                status='success',
                message='Bug successful!',
                data=serializer.data,
                code=status.HTTP_201_CREATED
            ).get_response()
        
        return CustomApiResponse(
            status='error',
            message='Bug Create failed',
            data=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        ).get_response()

    def patch(self, request):
        """
        Partial update of a Bug.
        Requires 'bug_id' query parameter.
        """
        bug_id = request.query_params.get("bug_id")
        if not bug_id:
            return CustomApiResponse(
                status="error",
                message="Bug ID is required for update.",
                data={},
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()

        try:
            bug = self.queryset.get(id=bug_id)
        except BugModel.DoesNotExist:
            return CustomApiResponse(
                status="error",
                message="Bug not found.",
                data={},
                code=status.HTTP_404_NOT_FOUND
            ).get_response()

        serializer = self.serializer_class(bug, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomApiResponse(
                status="success",
                message="Bug updated successfully.",
                data=serializer.data,
                code=status.HTTP_200_OK
            ).get_response()

        return CustomApiResponse(
            status="error",
            message="Bug update failed.",
            data=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        ).get_response()
    

    def delete(self, request):
        """
        Delete a Bug.
        Requires 'bug_id' query parameter.
        """
        bug_id = request.query_params.get("bug_id")
        if not bug_id:
            return CustomApiResponse(
                status="error",
                message="Bug ID is required for deletion.",
                data={},
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()

        try:
            bug = self.queryset.get(id=bug_id)
            bug.delete()
            return CustomApiResponse(
                status="success",
                message="Bug deleted successfully.",
                data={},
                code=status.HTTP_204_NO_CONTENT
            ).get_response()
        except BugModel.DoesNotExist:
            return CustomApiResponse(
                status="error",
                message="Bug not found.",
                data={},
                code=status.HTTP_404_NOT_FOUND
            ).get_response()
        

class CommentCRUDView(APIView):
    """
    Handles CRUD operations for CommentModel.
    
    Methods:
    - GET: Retrieve all Comment or a specific Comment by ID.
    - POST: Create a new Comment.
    - PATCH: Partially update a Comment.
    - DELETE: Delete a Comment.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = CommentModel.objects.all()

    def get(self, request):
        """
        Retrieve a specific Comment by ID (if provided),
        or return a list of all CommentModel.
        """
        comment_id = request.query_params.get("comment_id")

        if comment_id:
            # Try to fetch specific comment by ID
            try:
                comment = self.queryset.get(id=comment_id)
                serializer = self.serializer_class(comment)
                return CustomApiResponse(
                    status="success",
                    message="Comment retrieved successfully.",
                    data=serializer.data,
                    code=status.HTTP_200_OK
                ).get_response()
            except CommentModel.DoesNotExist:
                # If comment not found, return custom 404 response
                return CustomApiResponse(
                    status="error",
                    message="Comment not found.",
                    data={},
                    code=status.HTTP_404_NOT_FOUND
                ).get_response()
        else:
            # If no comment_id is given, return all comment
            bugs = self.queryset.all()
            serializer = self.serializer_class(bugs, many=True)
            return CustomApiResponse(
                status="success",
                message="All comment retrieved successfully.",
                data=serializer.data,
                code=status.HTTP_200_OK
            ).get_response()
        

    def post(self, request):
        current_user = request.user
        data = request.data.copy()
        data["commenter"] = current_user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return CustomApiResponse(
                status='success',
                message='Comment successful!',
                data=serializer.data,
                code=status.HTTP_201_CREATED
            ).get_response()
        
        return CustomApiResponse(
            status='error',
            message='Comment Create failed',
            data=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        ).get_response()

    def patch(self, request):
        """
        Partial update of a Comment.
        Requires 'comment_id' query parameter.
        """
        comment_id = request.query_params.get("comment_id")
        if not comment_id:
            return CustomApiResponse(
                status="error",
                message="Comment ID is required for update.",
                data={},
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()

        try:
            comment = self.queryset.get(id=comment_id)
        except CommentModel.DoesNotExist:
            return CustomApiResponse(
                status="error",
                message="Comment not found.",
                data={},
                code=status.HTTP_404_NOT_FOUND
            ).get_response()

        serializer = self.serializer_class(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomApiResponse(
                status="success",
                message="Comment updated successfully.",
                data=serializer.data,
                code=status.HTTP_200_OK
            ).get_response()

        return CustomApiResponse(
            status="error",
            message="Comment update failed.",
            data=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        ).get_response()
    

    def delete(self, request):
        """
        Delete a Comment.
        Requires 'comment_id' query parameter.
        """
        comment_id = request.query_params.get("comment_id")
        if not comment_id:
            return CustomApiResponse(
                status="error",
                message="Comment ID is required for deletion.",
                data={},
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()

        try:
            comment = self.queryset.get(id=comment_id)
            comment.delete()
            return CustomApiResponse(
                status="success",
                message="Comment deleted successfully.",
                data={},
                code=status.HTTP_204_NO_CONTENT
            ).get_response()
        except CommentModel.DoesNotExist:
            return CustomApiResponse(
                status="error",
                message="Comment not found.",
                data={},
                code=status.HTTP_404_NOT_FOUND
            ).get_response()
        



class AssignedBugsView(APIView):
    """
    API View to list all bugs assigned to the any authenticated user or current user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.query_params.get("user_id")
        current_user = request.user

        if user:
            bugs = BugModel.objects.filter(assigned_to=user)
        else:
            bugs = BugModel.objects.filter(assigned_to=current_user)
          
        serializer = BugSerializer(bugs, many=True)
        return CustomApiResponse(
            status="success",
            message="Bugs assigned to user retrieved successfully.",
            data=serializer.data,
            code=status.HTTP_200_OK
        ).get_response()