import os
import sys
import subprocess
from runner import discover
from runner import Asset, EAssetType
base_path = sys.argv[1] if len(sys.argv) >= 2 else "."

def get_extractor_command(asset):
    args = [ './ude-tool' ]
    args = args + [ '--pkgver', '513' ]
    args = args + [ '--asset', asset.path ]
    if asset.uexp_file:
        args = args + [ '--uexp', asset.uexp_file ]
    args = args + [ '--output', os.sep.join([asset.directory, asset.name + '.json']) ]
    args = args + [ 'export' ]
    return args

def get_cleaning_command(asset):
    args = [ 'python', 'json-cleanup.py' ]
    args = args + [ os.sep.join([asset.directory, asset.name + '.json']) ]
    output_directory = asset.directory.replace(base_path, 'artifacts')
    args = args + [ os.sep.join([output_directory, asset.name + '.json']) ]
    # Ensure the directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    return args

def delete_failed_assets(asset):
    return os.path.exists(os.sep.join([asset.directory, asset.name + '.json']))

discover([
    r"^(?!(SM)|M|T\_)(.*)\.uasset$",
    r"^(?!(SM)|T\_)(.*)\.umap$"
], base_path) \
    .cast_as(Asset, EAssetType.ASSET, selector=r"^(.*)\.uasset$") \
    .cast_as(Asset, EAssetType.MAP, selector=r"^(.*)\.umap$") \
    .run_process_for_each(get_extractor_command, max_simultaneous=12) \
    .filter(delete_failed_assets) \
    .run_process_for_each(get_cleaning_command, max_simultaneous=12)