import os
import json
from app.app import connexionApp as app

ROOT_PATH = os.environ.get('ROOT_PATH', '/covid19/')
DEBUG_PORT = json.loads(os.environ.get('DEBUG_PORT', 'null'))
DEBUG = json.loads(os.environ.get('DEBUG', 'true'))
# HOST = os.environ.get('HOST', '0.0.0.0')
PORT = json.loads(os.environ.get('PORT', '8080'))

if DEBUG_PORT is not None:
  import logging
  logging.warn('DEBUG_PORT is deprecated, please use DEBUG (true/false), and PORT')
  if os.environ.get('DEBUG') is None:
    DEBUG = True
  if os.environ.get('PORT') is None:
    PORT = DEBUG_PORT

# TODO: Add `HOST` when DB `HOST` is fully removed
print(f'Application at http://0.0.0.0:{PORT}{ROOT_PATH}')
print(f'Swagger UI at http://0.0.0.0:{PORT}{ROOT_PATH}ui/')
app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
