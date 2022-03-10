import random

def memepic(ask):
    if ask == '啪':
        pa_list = ['啪1','啪2','啪3']
        re = '/memepicture/' + random.choice(pa_list) + '.jpg'
        return re

print(memepic('啪'))