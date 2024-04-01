from django.db import models
import time
import pymysql
import re
import tkinter as tk
from bs4 import BeautifulSoup
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.edge.options import Options


# Create your models here.
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    # age = models.IntegerField()


class RootInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)


class Aim(models.Model):
    name = models.CharField(max_length=32)
    user_name = models.CharField(max_length=32)
    birthday = models.CharField(max_length=12)
    gender = models.CharField(max_length=12)


class RootBilibili(models.Model):
    label = models.CharField(max_length=64)
    user_name = models.CharField(max_length=32)
    aim_name = models.CharField(max_length=32)


class UserBilibili(models.Model):
    label = models.CharField(max_length=64)
    user_name = models.CharField(max_length=32)
    aim_name = models.CharField(max_length=32)


class RootBiliT(models.Model):
    user_name = models.CharField(max_length=32)
    aim_name = models.CharField(max_length=32)
    label = models.CharField(max_length=64)


class Label(models.Model):
    label_pro = models.CharField(max_length=64)


class RootData(models.Model):
    text = models.CharField(max_length=64)
    label = models.CharField(max_length=64, null=True)
