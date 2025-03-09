import yaml

with open('../materials/todo.yml', 'r') as todo_file:
    todo = yaml.safe_load(todo_file)

files_to_copy = todo['server']['exploit_files']
packages = todo['server']['install_packages']

deploy = {
    'name': 'Install Packages and Execute Scripts',
    'become': True,
    'tasks': [
        {
            'name': 'Install packages',
            'apt': {
                'name': packages,
                'state': 'present'
            }
        },
        {
            'name': 'Copy files to remote server',
            'copy': {
                'src': "{{ item }}", 'dest': "{{ item }}"
            },
            'loop': files_to_copy  # Loop through the list of files
        },
        {
            'name': 'Execute the consumer script',
            'command': (
                "python3 exploit.py && "
                "python3 consumer.py -e {}, {}".format(
                    todo['bad_guys'][0], todo['bad_guys'][1]
                )
            ),
        }
    ]
}
output_file = '../materials/deploy.yml'

with open(output_file, 'w') as yaml_file:
    yaml_file.write('---\n')
    yaml.dump(deploy, yaml_file, default_flow_style=False)
