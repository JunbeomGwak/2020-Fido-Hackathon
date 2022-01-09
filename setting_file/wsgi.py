import os, sys
from django.core.wsgi import get_wsgi_application
 
path = os.path.abspath(__file__+'/../..')
if path not in sys.path:
    sys.path.append(path)
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fido_project.settings")
application = get_wsgi_application()