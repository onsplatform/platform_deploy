import os

SCHEMA = {
    'tst': {
        'uri': os.environ.get('SCHEMA_URI', 'http://localhost:9092/api/v1/')
    },
    'hmg': {
        'uri': os.environ.get('SCHEMA_URI', 'http://localhost:9092/api/v1/')
    },
    'prd': {
        'uri': os.environ.get('SCHEMA_URI', 'http://localhost:9092/api/v1/')
    }
}

DISCOVERY = {
    'tst': {
        'uri': os.environ.get('DISCOVERY_URI', 'http://localhost:8099/')
    },
    'hmg': {
        'uri': os.environ.get('DISCOVERY_URI', 'http://localhost:8099/')
    },
    'prd': {
        'uri': os.environ.get('DISCOVERY_URI', 'http://localhost:8099/')
    }
}

CORE_API = {
    'tst': {
        'uri': os.environ.get('COREAPI_URI', 'http://localhost:9110/core/')
    },
    'hmg': {
        'uri': os.environ.get('COREAPI_URI', 'http://localhost:9110/core/')
    },
    'prd': {
        'uri': os.environ.get('COREAPI_URI', 'http://localhost:9110/core/')
    }
}

REGISTRY = {
    'uri': os.environ.get('IMAGE_REGISTRY', 'localhost:5000'),
    'username': os.environ.get('IMAGE_REGISTRY_USERNAME', 'username'),
    'password': os.environ.get('IMAGE_REGISTRY_PASSWORD', 'password'),
}