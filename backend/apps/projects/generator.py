class ProjectGenerator:
    """
    Generates the initial file structure for a student project.
    """
    
    @staticmethod
    def generate_scaffold(template, user):
        """
        Merges the template's scaffold with user-specific metadata.
        Returns a JSON structure of files.
        """
        scaffold = template.scaffold_config.copy()
        
        # Inject a personalized README
        readme_content = (
            f"# {template.title}\n"
            f"**Student:** {user.first_name} {user.last_name}\n"
            f"**Started:** {user.date_joined}\n\n"
            f"{template.description}\n"
        )
        
        scaffold['README.md'] = readme_content
        
        # Ensure a main entry point exists
        if 'main.py' not in scaffold:
            scaffold['main.py'] = "# Write your code here\n"

        return scaffold