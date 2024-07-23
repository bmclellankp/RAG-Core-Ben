import os
import json
import subprocess

def run():
    import os
    import json
    import subprocess
    file_path = os.path.join(os.getcwd(), 'templated_tests\\app.py')
    cwd = os.getcwd()
    return file_path, cwd

class Context:
    def __init__(self):
        pass
        # , root_directory, target_file):
        # self.root_directory = root_directory
        # self.target_file = target_file

    def run(self):
        import os
        import json
        import subprocess
        self.target_file = os.path.join(os.getcwd(), 'templated_tests\\app.py')
        self.root_directory = os.getcwd()
    def generate_directory_structure(self):
        dir_structure = {}
        root_path_parts = self.root_directory.split(os.sep)
        root_depth = len(root_path_parts)

        for dirpath, dirnames, filenames in os.walk(self.root_directory):
            path_parts = dirpath.split(os.sep)
            subdir = dir_structure

            # Only include the part of the path that is relative to the root_directory
            for part in path_parts[root_depth:]:
                subdir = subdir.setdefault(part, {})
            
            # Add filenames to the current directory in the structure
            subdir['files'] = filenames
        return dir_structure
    
    @staticmethod
    def save_structure_to_json(structure, output_file):
        with open(output_file, 'w') as f:
            json.dump(structure, f, indent=4)

    def parse_dot_file(self, dot_file):
        with open(dot_file, 'r') as f:
            lines = f.readlines()

        dependencies = {}
        for line in lines:
            if '->' in line:
                parts = line.strip().strip(';').split('->')
                src = parts[0].strip().strip('"')
                dst = parts[1].strip().strip('"')
                if src not in dependencies:
                    dependencies[src] = []
                dependencies[src].append(dst)

        return dependencies

    def generate_dependency_graph(self):
        dot_output_file = 'deps.dot'
        command = [
            'pydeps', 
            self.target_file, 
            '--show-deps', 
            '--max-bacon', '2', 
            '--dot', dot_output_file
        ]
        subprocess.run(command, shell=True, check=True)
        dependency_json = self.parse_dot_file(dot_output_file)
        return dependency_json
    
    def process_file_with_context(self):
        context_json = self.generate_directory_structure()
        dependency_json = self.generate_dependency_graph()

        with open(self.target_file, 'r') as file:
            file_content = file.read()
        
        input_data = {
            "context": context_json,
            "dependencies": dependency_json,
            "file_content": file_content
        }
        return input_data