import pytest
from apps.cars.models import Color, Car


@pytest.mark.django_db
def test_color_creation_update_delete():
    color_name = 'Purple'
    color = Color.objects.create(name=color_name)
    assert color.name == color_name
    assert Color.objects.count() == 5

    new_color_name = 'Midnight Blue'
    color.name = new_color_name
    color.save()
    assert color.name == new_color_name
    assert Color.objects.count() == 5

    color.delete()
    assert Color.objects.count() == 4


@pytest.mark.django_db
def test_car_creation_update_delete():
    car_name = 'Car1'
    car_length = 100.50
    car_weight = 200.75
    car_velocity = 60
    color_name = 'Red'

    # Create a color
    color = Color.objects.create(name=color_name)

    # Create a car with the created color
    car = Car.objects.create(
        name=car_name,
        color=color,
        length=car_length,
        weight=car_weight,
        velocity=car_velocity
    )

    assert car.name == car_name
    assert car.length == car_length
    assert car.weight == car_weight
    assert car.velocity == car_velocity
    assert car.color.name == color_name
    assert Car.objects.count() == 13

    car.name = 'Car2'
    car.length = 200.50
    car.weight = 300.75
    car.save()

    assert car.name == 'Car2'
    assert car.length == 200.50
    assert car.weight == 300.75
    assert Car.objects.count() == 13

    car.delete()
    assert Car.objects.count() == 12
