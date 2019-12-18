import os

SCHEMA = {
    'tst': {
        'uri': os.environ.get('SCHEMA_URI', 'http://localhost:8002/api/v1/')
    },
    'hmg': {
        'uri': os.environ.get('SCHEMA_URI', 'http://localhost:8002/api/v1/')
    },
    'prd': {
        'uri': os.environ.get('SCHEMA_URI', 'http://localhost:8002/api/v1/')
    }
}

REGISTRY = {
    'uri': os.environ.get('IMAGE_REGISTRY', 'localhost:5000')
}
