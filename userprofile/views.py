from rest_framework.response import Response
from rest_framework import status
from .serializers import UserProfileSerializer

def create_userprofile(request):
    try:
        required_fields = ['category']
        if not all(field in request.data for field in required_fields):
            return Response({
                'error': 'Missing required fields',
                'required': required_fields
            }, status=status.HTTP_400_BAD_REQUEST)
        profile_data = {
            'category': request.data.get('category', []),
            'description': request.data.get('description', []),
            'tags': request.data.get('tags', []),
            'recentChats': request.data.get('recentChats', []),
            'prefor': request.data.get('prefor', []),
            'characterstics': request.data.get('characterstics', []),
            'additionalInfo': request.data.get('additionalInfo', {})
        }
        # UserProfile 생성
        serializer = UserProfileSerializer(data=profile_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'UserProfile created successfully',
                'data': {'userID' : serializer.data['userID']}
            }, status=status.HTTP_201_CREATED)
        else:
            serializer.save()
            return Response({
                'message': 'UserProfile update complete',
                'data': {'userID' : serializer.data['userID']}
            }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)