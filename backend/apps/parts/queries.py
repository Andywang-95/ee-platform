from django.db.models import Q

from apps.parts.configuration import TYPE_FIELD, PartType
from apps.parts.models import Part


def list_parts(*, part_type: PartType, search='', filters=None, ordering=''):
    """Parts of one type, narrowed by keyword and exact-match filters.

    Callers validate `filters` and `ordering` against the type's configuration
    first; this function trusts them.
    """
    queryset = Part.objects.filter(**{TYPE_FIELD: part_type.code})

    if search:
        matches = Q()
        for field in part_type.search_fields:
            matches |= Q(**{f'{field}__icontains': search})
        queryset = queryset.filter(matches)

    if filters:
        queryset = queryset.filter(**filters)

    # SQL Server cannot paginate an unordered query, and `pk` as the last key
    # keeps pages stable when the chosen column has repeated values.
    return queryset.order_by(ordering or part_type.list_fields[0], 'pk')


def filter_options(*, part_type: PartType):
    """The distinct values present in each filterable column of one type."""
    parts = Part.objects.filter(**{TYPE_FIELD: part_type.code})
    return {
        field: list(
            parts.exclude(**{f'{field}__isnull': True})
            .exclude(**{field: ''})
            .values_list(field, flat=True)
            .distinct()
            .order_by(field)
        )
        for field in part_type.filter_fields
    }
