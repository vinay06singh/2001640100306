from rest_framework import viewsets
from .models import Number
from .serializers import NumberSerializer

class NumberViewSet(viewsets.ModelViewSet):
    queryset = Number.objects.all()
    serializer_class = NumberSerializer
