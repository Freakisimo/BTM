from distutils.core import setup
from glob import glob
import py2exe
import os
 
def add_path_tree( base_path, path, skip_dirs=[ '.svn', '.git' ]):
  path = os.path.join( base_path, path )
  partial_data_files = []
  for root, dirs, files in os.walk( os.path.join( path )):
    sample_list = []
    for skip_dir in skip_dirs:
      if skip_dir in dirs:
        dirs.remove( skip_dir )
    if files:
      for filename in files:
        sample_list.append( os.path.join( root, filename ))
    if sample_list:
      partial_data_files.append((
        root.replace(
          base_path + os.sep if base_path else '',
          '',
          1
        ),
        sample_list
      ))
  return partial_data_files

py2exe_options = {
  'py2exe': {
    'compressed': 1,
    'optimize': 2,
    'ascii': 1,
    'bundle_files': 1,
    'dist_dir': 'setup',
    'packages': [ 'encodings' ],
    'excludes' : [
      'pywin',
      'pywin.debugger',
      'pywin.debugger.dbgcon',
      'pywin.dialogs',
      'pywin.dialogs.list',
      'Tkconstants',
      'Tkinter',
      'tcl',
    ],
    'dll_excludes': [ 'w9xpopen.exe', 'MSVCR71.dll', 'MSVCP90.dll'],
    'includes': [
      ########
      # Site imports
      'graficas.models',
      'graficas.views',
      #reportes.urls
      'manage',
      'treemaps.urls',
      'treemaps.settings',
      ########
      # mass django import
      'django.conf.urls.shortcut',
      'django.contrib.admin',
      'django.contrib.admin.templatetags.log',
      'django.contrib.admin.views.main',
      'django.contrib.auth',
      'django.contrib.auth.backends',
      'django.contrib.auth.middleware',
      'django.contrib.auth.middleware',
      'django.contrib.auth.views',
      'django.contrib.auth.context_processors',
      'django.contrib.contenttypes',
      'django.contrib.messages.context_processors',
      'django.contrib.messages.middleware',
      'django.contrib.messages.storage.fallback',
      'django.contrib.sessions',
      'django.contrib.sessions.backends.db',
      'django.contrib.sessions.middleware',
      'django.contrib.sites',
      'django.core.cache.backends',
      'django.core.cache.backends.locmem',
      'django.core.context_processors',
      'django.core.servers.basehttp',
      'django.db.backends.sqlite3',
      'django.db.backends.sqlite3.base',
      'django.db.backends.sqlite3.client',
      'django.db.backends.sqlite3.creation',
      'django.db.backends.sqlite3.introspection',
      'django.middleware.common',
      'django.middleware.doc',
      'django.template.defaultfilters',
      'django.template.defaulttags',
      'django.template.loader_tags',
      'django.template.loaders.app_directories',
      'django.template.loaders.filesystem',
      'django.templatetags.i18n',
      'django.utils.html_parser',
      'django.utils.timezone',
      'django.utils.simplejson',
      'django.views.defaults',
      'django.views.i18n',
      'django.views.static',
      #Las necesarias para potencial
      'django.shortcuts',
      'django.db.models',
      'django.db.models.query',
      'django.db.models.sql.compiler',
      'django.core.context_processors',
      'django.template',  
      'django.views.decorators.csrf',
      # importar numpy, pandas y demas ocupadas en este sitio
      'os',
      'numpy.*',
      'numpy.linalg.*',
      'pandas',
      'collections',
      'operator',
      'cherrypy',
      'translogger',
      'HTMLParser',
      'compiler',
      'pytz',
      'pytz.exceptions',
      'pytz.lazy',
      'pytz.reference',
      'pytz.tzfile',
      'pytz.tzinfo',
       # also used by django?
      'email.mime.audio',
      'email.mime.base',
      'email.mime.image',
      'email.mime.message',
      'email.mime.multipart',
      'email.mime.nonmultipart',
      'email.mime.text',
      'email.charset',
      'email.encoders',
      'email.errors',
      'email.feedparser',
      'email.generator',
      'email.header',
      'email.iterators',
      'email.message',
      'email.parser',
      'email.utils',
      'email.base64mime',
      'email.quoprimime',
    ],
  }
}


# Take the first value from the environment variable PYTHON_PATH
python_path = os.environ[ 'path' ].split( ';' )[ 0 ]

#Crear ruta del proyecto
ruta_proyecto = os.path.dirname(os.path.realpath(__file__))
ruta_proyecto = os.path.normpath( ruta_proyecto + '/treemaps/' )
 
#django_admin_path = os.path.normpath( python_path + '/lib/site-packages/django/contrib/admin' )
py2exe_data_files = []

py2exe_data_files += add_path_tree( ruta_proyecto, 'static' )
 
setup(
  options=py2exe_options,
  data_files=py2exe_data_files,
  zipfile = None,
  console=[ 'cuanti_boheringer.py' ],
)