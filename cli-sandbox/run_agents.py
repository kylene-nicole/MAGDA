import os
import questionary
import shutil
from shutil import copytree, ignore_patterns
from tabulate import tabulate

class MagdaCLI:
    def __init__(self):
        self.example_data = None
        self.project = None
        self.selected_grant_opportunities = None
        # Define the base path relative to this script file location
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    def run(self):
        self.magda_path = self.ensure_magda_directory()
        
        while self.project is None:
            self.choose_project()
        
        self.invoke_search_agents()
        self.select_grant_opportunities()
        self.invoke_drafting_agents()

    def ensure_magda_directory(self):
        magda_path = os.path.expanduser('~/MAGDA')
        template_path = os.path.join(magda_path, 'template')

        # Use a relative path for the source template
        source_template_path = os.path.join(self.base_path, 'magda-template')

        if not os.path.exists(magda_path):
            os.makedirs(magda_path)
            if os.path.exists(source_template_path):
                shutil.copytree(source_template_path, template_path)
                print(f'Copied template from {source_template_path} to {template_path} ✅')
            else:
                print(f'Source template directory {source_template_path} does not exist.')
        else:
            print('MAGDA directory already exists. ✅')

        return magda_path

    def choose_project(self):
        projects = [d for d in os.listdir(self.magda_path) if os.path.isdir(os.path.join(self.magda_path, d)) and d != 'template']
        
        action = questionary.select(
            "Do you want to use a previous project or create a new one?",
            choices=['use', 'create']
        ).ask()

        if action == 'create':
            project_name = questionary.text("Enter new project name:").ask()
            new_project_path = os.path.join(self.magda_path, project_name)
            if not os.path.exists(new_project_path):
                copytree(os.path.join(self.magda_path, 'template'), new_project_path, ignore=ignore_patterns('*.pyc', 'tmp*'))
                print(f'Created new project "{project_name}"')
            else:
                print(f'Project "{project_name}" already exists.')
            self.project = project_name
        elif action == 'use' and projects:
            project_name = questionary.select("Select a project to use:", choices=projects).ask()
            # Perform actions with the selected project here
            self.project = project_name
            # list_files(os.path.join(self.magda_path, project_name))
        else:
            print("No projects available to use. Please create a new project.")

    def invoke_search_agents(self):
        action = questionary.select(
            "Do you want to find grants associated with this project?",
            choices=['yes', 'no']
        ).ask()

        if action == 'yes':
            print("Finding grants...")
            # save as JSON and CSV here
            self.example_data = [
                ["Project Name", "Description", "URL"],
                ["Project1", "An example project.", "https://example.com/project1"],
                ["Project2", "Another example project.", "https://example.com/project2"]
            ]
            # create CSV in the project directory in MAGDA
            self.display_table()
            
        if action == 'no':
            print("No action taken.")

    def select_grant_opportunities(self):
        if self.example_data:
            selected_projects = questionary.checkbox(
                "Select projects to use:",
                choices=[row[0] for row in self.example_data[1:]]
            ).ask()
            print("You selected:")
            for project in selected_projects:
                print(project)
            self.selected_grant_opportunities = selected_projects
        else:
            print("No projects available to use. Please create a new project.")

    def display_table(self):
        print(tabulate(self.example_data, headers='firstrow', tablefmt='grid'))
            
    def list_files(self, directory):
        """Lists files in the given directory"""
        for filename in os.listdir(directory):
            print(filename)

    def invoke_drafting_agents(self):
        # create a new file in the project directory for each selected grant opportunity
        pass


if __name__ == "__main__":
    cli = MagdaCLI()
    cli.run()
