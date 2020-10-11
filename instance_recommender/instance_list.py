import json
import pandas

def get_region_file_content(region):
    try:
        import importlib.resources as pkg_resources
    except ImportError:
        # Try backported to PY<37 `importlib_resources`.
        import importlib_resources as pkg_resources

    from .static import regions  # relative-import the *package* containing the templates
    return pandas.DataFrame(json.loads(pkg_resources.read_text(regions, region)))


def get_list_of_instances(constraints):
    df = get_region_file_content(constraints["region"])
    if 'vcpus' in constraints:
        df =  df[(df.vcpus >= constraints['vcpus']['min']) & (df.vcpus <= constraints['vcpus']['max'])]
    if 'memory' in constraints:
        df =  df[(df.memory >= constraints['memory']['min']) & (df.memory <= constraints['memory']['max'])]
    df = df[df.arch == constraints['arch']]
    return df

