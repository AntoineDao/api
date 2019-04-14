"""Mix openapi documentation for different pollination micro-services into one!"""
import requests
import json
import yaml


def main(openapi_links):
    # read base data from openapi.yaml
    base_openapi = './spec/openapi.yaml'
    with open(base_openapi) as inf:
        content = inf.read()
    
    # load base spec
    openapi_doc = yaml.load(content)
    
    # add empty fields
    openapi_doc['paths'] = {}
    openapi_doc['components'] = {'schemas': {}, 'securitySchemes': {}}
    
    # collect fields from micro-service openapi schemas
    print('loading documentation for micro-services...')
    for link in openapi_links:
        r = requests.get(link)
        response = r.json()
        for path, value in response['paths'].items():
            openapi_doc['paths'][path] = value
        for schema, value in response['components']['schemas'].items():
            openapi_doc['components']['schemas'][schema] = value
        # this is the same for all schemas
        openapi_doc['components']['securitySchemes'] = \
            response['components']['securitySchemes']

        r.close()

    print('writing openapi.json...')
    with open('openapi.json', 'w') as outf:
        json.dump(openapi_doc, outf)

    print('writing openapi.yaml...')
    with open('openapi.yaml', 'w') as outf:
        outf.write(yaml.dump(openapi_doc, default_flow_style=False))

    print('done!')


if __name__ == '__main__':
    # this should be updated to files from gh-pages branches of each microservice
    # repository
    openapi_links = [
        'https://gist.githubusercontent.com/mostaphaRoudsari/0045cc5121c0ef2e11dd1646520103f3/raw/96851959c80fc39cc0d406ac0ea27d1a28951846/sensor_grid_openapi.json',
        'https://gist.githubusercontent.com/mostaphaRoudsari/0045cc5121c0ef2e11dd1646520103f3/raw/f20fde61300b821f93f0d003007796f805fb1dac/model_openapi.json',
        'https://gist.githubusercontent.com/mostaphaRoudsari/0045cc5121c0ef2e11dd1646520103f3/raw/a2ad251c010207b7c96281029a1d1be4b5aef0e7/simulation_openapi.json'
    ]

    main(openapi_links)
