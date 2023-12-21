from __future__ import print_function
from djangoplicity.products.models import *


ps = Poster.objects.exclude(type='C')

for p in ps:
    print(p.type)
