import pytest
from django.urls import reverse

from apps.parts.models import Part

pytestmark = pytest.mark.django_db(databases=['default', 'parts'])

LIST_URL = reverse('parts:list')


@pytest.fixture
def user_client(client, django_user_model):
    client.force_login(django_user_model.objects.create_user('reader'))
    return client


@pytest.fixture
def parts():
    return Part.objects.bulk_create(
        [
            Part(
                id=1,
                part_number='RES-0402-10K',
                table_name='R',
                value='10K',
                tolerance='1%',
                package='0402',
                manufacturer='Yageo',
                description='RES 10K 0402',
                remark='Preferred part.',
            ),
            Part(
                id=2,
                part_number='RES-0603-10K',
                table_name='R',
                value='10K',
                tolerance='5%',
                package='0603',
                manufacturer='Yageo',
                description='RES 10K 0603',
            ),
            Part(
                id=3,
                part_number='RES-0402-1K',
                table_name='R',
                value='1K',
                tolerance='1%',
                package='0402',
                manufacturer='Samsung',
                description='RES 1K 0402',
            ),
            Part(
                id=4,
                part_number='CAP-0402-100nF',
                table_name='C',
                value='100nF',
                voltage_rating='16V',
                package='0402',
                manufacturer='Murata',
                description='CAP 100nF 0402',
            ),
        ]
    )


def part_numbers(response):
    return [row['part_number'] for row in response.json()['results']]


@pytest.mark.parametrize(
    'url',
    [
        LIST_URL + '?type=R',
        reverse('parts:types'),
        reverse('parts:filter-options', args=['R']),
        reverse('parts:detail', args=[1]),
    ],
)
def test_anonymous_requests_are_rejected(client, parts, url):
    assert client.get(url).status_code == 403


def test_types_describe_each_configured_type(user_client):
    response = user_client.get(reverse('parts:types'))

    assert response.status_code == 200
    types = {part_type['code']: part_type for part_type in response.json()}
    assert set(types) == {'R', 'C', 'L', 'IC'}
    assert types['R']['label'] == '電阻'
    assert types['R']['list_fields'][1] == {'name': 'value', 'label': '阻值'}
    assert types['R']['remark_field'] == 'remark'


def test_list_returns_only_the_requested_type(user_client, parts):
    response = user_client.get(LIST_URL, {'type': 'C'})

    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert part_numbers(response) == ['CAP-0402-100nF']


def test_list_rows_hold_the_list_fields_id_and_remark(user_client, parts):
    row = user_client.get(LIST_URL, {'type': 'R'}).json()['results'][0]

    assert set(row) == {
        'id',
        'part_number',
        'value',
        'tolerance',
        'power_rating',
        'package',
        'manufacturer',
        'description',
        'remark',
    }
    assert row['remark'] == 'Preferred part.'


def test_list_requires_a_known_type(user_client, parts):
    assert user_client.get(LIST_URL).status_code == 400
    assert user_client.get(LIST_URL, {'type': 'X'}).status_code == 400


def test_search_matches_any_search_field_ignoring_case(user_client, parts):
    assert part_numbers(user_client.get(LIST_URL, {'type': 'R', 'search': '0603'})) == [
        'RES-0603-10K'
    ]
    assert part_numbers(user_client.get(LIST_URL, {'type': 'R', 'search': 'res 1k'})) == [
        'RES-0402-1K'
    ]


def test_filters_combine(user_client, parts):
    response = user_client.get(LIST_URL, {'type': 'R', 'package': '0402', 'manufacturer': 'Yageo'})

    assert part_numbers(response) == ['RES-0402-10K']


def test_filter_on_a_field_outside_the_configuration_is_rejected(user_client, parts):
    response = user_client.get(LIST_URL, {'type': 'R', 'voltage_rating': '16V'})

    assert response.status_code == 400
    assert 'voltage_rating' in response.json()


def test_ordering_ascending_and_descending(user_client, parts):
    ascending = user_client.get(LIST_URL, {'type': 'R', 'ordering': 'package'})
    descending = user_client.get(LIST_URL, {'type': 'R', 'ordering': '-package'})

    assert part_numbers(ascending) == ['RES-0402-10K', 'RES-0402-1K', 'RES-0603-10K']
    assert part_numbers(descending) == ['RES-0603-10K', 'RES-0402-10K', 'RES-0402-1K']


def test_ordering_on_a_field_outside_the_list_is_rejected(user_client, parts):
    response = user_client.get(LIST_URL, {'type': 'R', 'ordering': 'remark'})

    assert response.status_code == 400
    assert 'ordering' in response.json()


def test_list_is_paginated(user_client, parts):
    response = user_client.get(LIST_URL, {'type': 'R', 'page_size': 2, 'page': 2})

    assert response.json()['count'] == 3
    assert part_numbers(response) == ['RES-0603-10K']
    assert response.json()['next'] is None
    assert response.json()['previous'] is not None


def test_filter_options_list_distinct_values_of_the_type(user_client, parts):
    response = user_client.get(reverse('parts:filter-options', args=['R']))

    assert response.status_code == 200
    assert response.json() == {
        'tolerance': ['1%', '5%'],
        'power_rating': [],
        'package': ['0402', '0603'],
        'manufacturer': ['Samsung', 'Yageo'],
    }


def test_filter_options_of_an_unknown_type_are_not_found(user_client):
    assert user_client.get(reverse('parts:filter-options', args=['X'])).status_code == 404


def test_detail_returns_every_labelled_field(user_client, parts):
    response = user_client.get(reverse('parts:detail', args=[4]))

    assert response.status_code == 200
    assert response.json()['part_number'] == 'CAP-0402-100nF'
    assert response.json()['voltage_rating'] == '16V'
    assert response.json()['table_name'] == 'C'


def test_detail_of_a_missing_part_is_not_found(user_client, parts):
    assert user_client.get(reverse('parts:detail', args=[999])).status_code == 404
