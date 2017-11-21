# -*- coding: utf-8 -*-
from django.db import models


class Data(models.Model):
    key = models.CharField(max_length=200)
    data = models.TextField()

    def __str__(self):
        return self.key
