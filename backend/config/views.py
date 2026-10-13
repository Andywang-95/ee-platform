from django.db import DatabaseError, connections
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.parts.models import Part
from config.db_routers import PARTS_DB

HealthSerializer = inline_serializer(
    name='Health',
    fields={
        'status': serializers.ChoiceField(choices=['ok', 'error']),
        'platform_db': serializers.BooleanField(),
        'parts_db': serializers.BooleanField(),
        'part_count': serializers.IntegerField(allow_null=True),
    },
)


class HealthView(APIView):
    """Report whether the backend can reach both of its databases."""

    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(responses={200: HealthSerializer, 503: HealthSerializer})
    def get(self, request):
        platform_db = self._can_query('default')
        part_count = self._count_parts()
        healthy = platform_db and part_count is not None
        return Response(
            {
                'status': 'ok' if healthy else 'error',
                'platform_db': platform_db,
                'parts_db': part_count is not None,
                'part_count': part_count,
            },
            status=200 if healthy else 503,
        )

    @staticmethod
    def _can_query(alias):
        try:
            with connections[alias].cursor() as cursor:
                cursor.execute('SELECT 1')
        except DatabaseError:
            return False
        return True

    @staticmethod
    def _count_parts():
        try:
            return Part.objects.using(PARTS_DB).count()
        except DatabaseError:
            return None
