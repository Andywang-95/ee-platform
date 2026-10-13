from django.db import models


class Part(models.Model):
    """One row of the existing parts table shared with Capture CIS.

    The columns below are assumptions until the real schema is available; see
    docs/domains/parts-schema-assumptions.md.
    """

    id = models.IntegerField(primary_key=True)
    part_number = models.CharField(max_length=50)
    table_name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    value = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    tolerance = models.CharField(max_length=20, blank=True, null=True)  # noqa: DJ001
    power_rating = models.CharField(max_length=20, blank=True, null=True)  # noqa: DJ001
    voltage_rating = models.CharField(max_length=20, blank=True, null=True)  # noqa: DJ001
    current_rating = models.CharField(max_length=20, blank=True, null=True)  # noqa: DJ001
    package = models.CharField(max_length=50, blank=True, null=True)  # noqa: DJ001
    manufacturer = models.CharField(max_length=100, blank=True, null=True)  # noqa: DJ001
    manufacturer_part_number = models.CharField(max_length=100, blank=True, null=True)  # noqa: DJ001
    schematic_part = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    pcb_footprint = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001
    remark = models.TextField(blank=True, null=True)  # noqa: DJ001

    class Meta:
        managed = False
        db_table = 'parts'

    def __str__(self):
        return self.part_number
