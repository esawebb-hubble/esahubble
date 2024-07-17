from .dev import *

# Make this unique, and don't share it with anybody.
SECRET_KEY = "g6ymvx$i1asv4k*g+nwfnx*3a1g&)^i6r9n6g4=f_$x^u(kwt8s"

# just in testing
CELERY_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_RESULT_BACKEND = 'db+sqlite:///results.db'
CELERY_BROKER_URL = 'memory://localhost//'
