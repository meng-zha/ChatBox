# -*- coding: utf-8 -*-

import random

def generateAddress():
    A = random.randint(224,239)
    B = random.randint(0,255)
    C = random.randint(0,255)
    D = random.randint(0,255)
    return ('{}.{}.{}.{}'.format(A,B,C,D))

def generatePort():
    return random.randint(5000,10000)