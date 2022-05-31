import yaml
import markdown

class MDParser():
    """Parses markdown files with YAML front-matter for trip
    reports. Places rendered markdown into a seperate attribute of the
    class for easy use."""

    def __init__(self, filename: str):
        self.filename = filename
        self.id = filename.split("/")[-1].split(".")[0]
        self.parse()

    def parse(self) -> None:
        """Parses the markdown file and returns the markdown and yaml
        front-matter."""

        with open(self.filename, "r") as f:
            md = f.read()

        yaml_start = md.find("---")
        yaml_end = md.find("---", yaml_start + 3)

        yaml_str = md[yaml_start + 3:yaml_end]
        md = md[yaml_end + 3:]

        self.yaml = yaml.safe_load(yaml_str.strip())
        
        # This just makes it easier to access the yaml data
        # from the template
        for key, value in self.yaml.items():
            setattr(self, key, value)
        
        self.md = markdown.markdown(md.strip(), extensions=['markdown.extensions.tables'])
