from rest_framework import viewsets
from .permissions import IsValidUser
from .models import CustomUser as User
from .serializers import UserUpdateSerializer

# Create your views here.
class UserUpdateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    http_method_names = ('patch', 'delete')
    permission_classes = [IsValidUser,]

