from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    city = models.ForeignKey('City', related_name='shops', on_delete=models.PROTECT)
    street = models.ForeignKey('Street', related_name='shops', on_delete=models.PROTECT)
    house = models.CharField(max_length=20)

    opening_time = models.TimeField()
    closing_time = models.TimeField()

    @property
    def city_name(self):
        return self.city.name

    @property
    def street_name(self):
        return self.street.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.name!r}, '
                f'{self.city!r}, '
                f'{self.house!r}, '
                f'{self.opening_time!r}, '
                f'{self.closing_time!r})')


class Street(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    city = models.ForeignKey('City', related_name='streets', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.name!r}, '
                f'{self.city!r})')


class City(models.Model):
    name = models.CharField(max_length=256, db_index=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'({self.name!r})')
