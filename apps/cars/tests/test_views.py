import pytest
from django.urls import reverse
from django.test import RequestFactory
from apps.cars.models import Car
from apps.cars.views import IndexView
from formencode.doctest_xml_compare import xml_compare
from lxml import etree


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.mark.django_db
def test_get_queryset(factory):
    request = factory.get(reverse('cars:index'))
    view = IndexView()
    view.request = request
    queryset = view.get_queryset()

    # Test no search keyword
    assert list(queryset) == list(Car.objects.order_by('name').all())

    # Test with search keyword
    request = factory.get(reverse('cars:index'), {'s': 'Mitsubishi'})
    view.request = request
    queryset = view.get_queryset()
    assert list(queryset) == list(Car.objects.filter(name__icontains='Mitsubishi').all())


@pytest.mark.django_db
def test_download_as_xml():
    cars = Car.objects.filter(name__icontains='Mitsubishi').order_by('name').all()

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
            <name>Mitsubishi Lancer</name>
            <length>170.00</length>
            <weight>220.00</weight>
            <velocity>200</velocity>
            <color>Blue</color>
        </car>
        <car>
            <name>Mitsubishi Mirage</name>
            <length>120.00</length>
            <weight>200.00</weight>
            <velocity>160</velocity>
            <color>Red</color>
        </car>
    </cars>"""
    compare1 = etree.fromstring(response.content.decode().strip())
    compare2 = etree.fromstring(expected_xml.strip())

    assert xml_compare(compare1, compare2) is True



@pytest.mark.django_db
def test_get(factory):
    # Test without download parameter
    request = factory.get(reverse('cars:index'))
    response = IndexView.as_view()(request)
    assert response.status_code == 200

    # Test with download parameter
    request = factory.get(reverse('cars:index'), {'download': 'true'})
    response = IndexView.as_view()(request)
    assert response.status_code == 200