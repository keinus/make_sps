import yaml
from app.schema.web_api import SpsProject, Csu

def parse_sps_project(file_path: str) -> SpsProject:
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    project_data = data.get('project', {})
    csu_list = [Csu(csu=item['csu'], dir=item['dir']) for item in project_data.get('csu', [])]
    return SpsProject(
        device=project_data['device'],
        version=project_data['version'],
        partnumber=project_data['partnumber'],
        checksum_type=project_data['checksum_type'],
        csu=csu_list
    )