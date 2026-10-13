from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.parts import queries
from apps.parts.configuration import FIELD_LABELS, PART_TYPES, REMARK_FIELD
from apps.parts.models import Part
from apps.parts.pagination import PartPagination
from apps.parts.serializers import PartPageSerializer, PartTypeSerializer

# Query parameters of the list API that are not column filters.
RESERVED_PARAMS = {'type', 'search', 'ordering', 'page', 'page_size'}


def describe(part_type):
    def fields(names):
        return [{'name': name, 'label': part_type.label_of(name)} for name in names]

    return {
        'code': part_type.code,
        'label': part_type.label,
        'list_fields': fields(part_type.list_fields),
        'detail_fields': fields(FIELD_LABELS),
        'search_fields': list(part_type.search_fields),
        'filter_fields': fields(part_type.filter_fields),
        'editable_fields': list(part_type.editable_fields),
        'remark_field': REMARK_FIELD,
    }


class PartTypeListView(APIView):
    """Every part type with its configuration."""

    @extend_schema(responses=PartTypeSerializer(many=True))
    def get(self, request):
        return Response([describe(part_type) for part_type in PART_TYPES.values()])


class PartFilterOptionsView(APIView):
    """The values that exist in each filterable column of one part type."""

    @extend_schema(responses=OpenApiTypes.OBJECT)
    def get(self, request, code):
        part_type = PART_TYPES.get(code)
        if part_type is None:
            raise NotFound(f'Unknown part type "{code}".')
        return Response(queries.filter_options(part_type=part_type))


class PartListView(APIView):
    """Parts of one type, with keyword search, column filters and sorting."""

    @extend_schema(
        operation_id='parts_list',
        parameters=[
            OpenApiParameter('type', OpenApiTypes.STR, required=True, description='Part type code'),
            OpenApiParameter('search', OpenApiTypes.STR, description='Keyword'),
            OpenApiParameter(
                'ordering', OpenApiTypes.STR, description='List field, prefix with - to reverse'
            ),
            OpenApiParameter('page', OpenApiTypes.INT),
            OpenApiParameter('page_size', OpenApiTypes.INT),
        ],
        description=(
            'Any other query parameter is an exact-match filter and must be one of '
            "the type's filter fields."
        ),
        responses=PartPageSerializer,
    )
    def get(self, request):
        params = request.query_params
        part_type = self._part_type(params)

        queryset = queries.list_parts(
            part_type=part_type,
            search=params.get('search', '').strip(),
            filters=self._filters(part_type, params),
            ordering=self._ordering(part_type, params),
        )

        paginator = PartPagination()
        page = paginator.paginate_queryset(
            queryset.values('id', *part_type.list_fields, REMARK_FIELD), request
        )
        return paginator.get_paginated_response(page)

    @staticmethod
    def _part_type(params):
        code = params.get('type')
        if not code:
            raise ValidationError({'type': ['This parameter is required.']})
        if code not in PART_TYPES:
            raise ValidationError({'type': [f'Unknown part type "{code}".']})
        return PART_TYPES[code]

    @staticmethod
    def _filters(part_type, params):
        filters = {name: params[name] for name in params if name not in RESERVED_PARAMS}
        unknown = sorted(set(filters) - set(part_type.filter_fields))
        if unknown:
            raise ValidationError(
                {name: [f'Cannot filter {part_type.code} parts by this field.'] for name in unknown}
            )
        return filters

    @staticmethod
    def _ordering(part_type, params):
        ordering = params.get('ordering', '')
        if ordering and ordering.removeprefix('-') not in part_type.list_fields:
            raise ValidationError(
                {'ordering': [f'Cannot sort {part_type.code} parts by "{ordering}".']}
            )
        return ordering


class PartDetailView(APIView):
    """Every platform-visible column of one part."""

    @extend_schema(responses=OpenApiTypes.OBJECT)
    def get(self, request, pk):
        part = get_object_or_404(Part.objects.values(*FIELD_LABELS), pk=pk)
        return Response(part)
