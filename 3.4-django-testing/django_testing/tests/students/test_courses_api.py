import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    course_factory()
    response = client.get('/api/v1/courses/1/')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1

@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)

@pytest.mark.django_db
def test_course_filter_id(client, course_factory):
    courses = course_factory(_quantity=10)
    test_id = courses[4].id
    response = client.get(f'/api/v1/courses/?id={test_id}')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1 and data[0]['id'] == test_id

@pytest.mark.django_db
def test_course_filter_name(client, course_factory):
    courses = course_factory(_quantity=10)
    test_name = courses[2].name
    response = client.get(f'/api/v1/courses/?name={test_name}')
    assert response.status_code == 200
    data = response.json()
    for d in data:
        assert d['name'] == test_name

@pytest.mark.django_db
def test_course_create(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'test course'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_course_update(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.patch(f'/api/v1/courses/{courses[5].id}/', data={'name': 'test course'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'test course'

@pytest.mark.django_db
def test_course_delete(client, course_factory):
    courses = course_factory(_quantity=10)
    count = Course.objects.count()
    response = client.delete(f'/api/v1/courses/{courses[5].id}/')
    assert response.status_code == 204
    assert Course.objects.count() == count - 1

@pytest.mark.django_db
@pytest.mark.parametrize('student_count, expected_status', [(2, 200),(3, 400)])
def test_max_student_per_course_limit(client, student_factory, course_factory,
        settings, student_count, expected_status):
    settings.MAX_STUDENTS_PER_COURSE = 2
    students = student_factory(_quantity=student_count)
    course = course_factory()
    response = client.patch(f'/api/v1/courses/{course.id}/',
                            {'students': [s.id for s in students]}, format='json')
    assert response.status_code == expected_status
