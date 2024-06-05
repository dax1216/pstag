import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.core.management import call_command
from apps.cars.models import Car
from apps.cars.views import IndexView


@pytest.fixture
def setup_db():
    call_command('loaddata', 'cars.json')  # Assuming the fixture file is named cars.json


@pytest.fixture
def factory():
    return RequestFactory()


def test_get_queryset(factory, setup_db):
    request = factory.get(reverse('cars:index'))
    view = IndexView()
    view.request = request
    queryset = view.get_queryset()

    # Test no search keyword
    assert list(queryset) == list(Car.objects.all())

    # Test with search keyword
    request.GET['s'] = 'Mitsubishi'
    queryset = view.get_queryset()
    assert list(queryset) == [Car.objects.get(name__icontains='Mitsubishi')]


def test_download_as_xml(setup_db):
    cars = Car.objects.all()
    response = IndexView.download_as_xml(cars)

    # Test if response is successful
    assert response.status_code == 200

    # Test if content type is application/xml
    assert response['Content-Type'] == 'application/xml'

    # Test if Content-Disposition is attachment and filename is cars.xml
    assert response['Content-Disposition'] == 'attachment; filename="cars.xml"'

    # Test if XML data is correct
    expected_xml = """<?xml version="1.0"?>
    <cars>
        <car>
            <name>Car1</name>
            <length>100</length>
            <weight>200</weight>
            <velocity>50</velocity>
            <color>Red</color>
        </car>
        <car>
            <name>Car2</name>
            <length>120</length>
            <weight>220</weight>
            <velocity>60</velocity>
            <color>Blue</color>
        </car>
    </cars>"""
    assert response.content.decode() == expected_xml.strip()


def test_get(factory, setup_db):
    # Test without download parameter
    request = factory.get(reverse('cars:index'))
    response = IndexView.as_view()(request)
    assert response.status_code == 200

    # Test with download parameter
    request = factory.get(reverse('cars:index'), {'download': 'true'})
    response = IndexView.as_view()(request)
    assert response.status_code == 200