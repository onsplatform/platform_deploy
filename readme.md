Basic commands:

1. Installation (path: /plataform_deploy/):
	1. pipenv --three
	2. pipenv install

2. Load environment (path: /plataform_deploy/):
	1. pipenv shell

3. Deploy entities (path: folder which contains an application of type 'domain' along with the respective plataform.json)
	1. python $path_to_plataform_deploy\main.py --create_entities --environment $environmentCode --platform $plataformaCode 
	2. Example: python c:\plataform_deploy\main.py --create_entities --environment tst --platform docker 

4. Build and deploy application's image (path: folder which contains an application of type 'process' or 'presentation' along with the respective plataform.json)
	1. python $path_to_plataform_deploy\main.py --build --environment $environmentCode --platform $plataformaCode 
	2. Example: python c:\plataform_deploy\main.py --build --environment tst --platform docker 
	
5. Deploy application's map and metadata (path: folder which contains an application of type 'process' or 'presentation' along with the respective plataform.json)
	1. python $path_to_plataform_deploy\main.py --register_schema --environment $environmentCode --platform $plataformaCode 
	2. Example: python c:\plataform_deploy\main.py --register_schema --environment tst --platform docker

6. Run a presentation app (path: folder which contains an application of type 'presentation' along with the respective plataform.json)
	1. python $path_to_plataform_deploy\main.py --run_presentation --environment $environmentCode --platform $plataformaCode 
	2. Example: python c:\plataform_deploy\main.py --run_presentation --environment tst --platform docker

The config_json file needs to respect the following structure:

    {
        "app": {
            "type": "presentation/process",
            "tecnology": "dotnet/go/python/etc",
            "name": "name_of_the_application",
            "container": "name_of_the_application_container",
            "version": "version_of_application",
            "date_begin_validity": "universal_date",
            "date_end_validity": "universal_date",
            "description": "description_of_application",
            "author": "name_of_the_author",
            "id": "uuid_of_application"
        },
        "solution": {
            "name": "name_of_the_solution",
            "description": "description_of_solution",
            "id": "uuid_of_solution",
            "id_domain": id_of_domain

        }
    }

Example:
    {
    "app": {
        "type": "presentation",
        "tecnology": "dotnet",
        "name": "crud",
		"container": "crud",
        "version": "1.0",
        "date_begin_validity": "2019-11-20T00:00",
        "date_end_validity": null,
        "description": "presentation application",
        "author": "Jon Doe",
        "id": "189c3686-3dt5-4ai5-81ae-4fa1035fe419"
        },
        "solution": {
            "name": "dummy solution",
            "description": "Simple description",
            "id": "a12d9e4d-c322-4ac2-9321-2f496fe3a116",
            "id_domain": 1
        }
    }
