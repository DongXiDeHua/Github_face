from django.db import models
from UI import models


def root_data(aim_name, user_name):
    result = models.RootBilibili.objects.filter(aim_name=aim_name, user_name=user_name)
    root_datas = {}
    root_datass = []
    for rootdata in result:
        if rootdata.label in root_datas:
            root_datas[rootdata.label] = +1
            print(rootdata.label)
        else:
            root_datas[rootdata.label] = 1
            print(rootdata.label)
    for key in root_datas:
        models.RootData.objects.create(text=key, label=None)
        print(key)
