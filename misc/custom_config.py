import json
import os
import copy
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--packer-template", dest="packer_template", type=Path)
parser.add_argument("--managed-image-name",
                    dest="managed_image_name",
                    type=str)
parser.add_argument("--managed-image-resource-group-name",
                    dest="managed_image_resource_group_name",
                    type=str)
parser.add_argument("--shared-image-gallery",
                    dest="shared_image_gallery",
                    action='store_true')

args = parser.parse_args()
packer_json = args.packer_template

with packer_json.open() as f:
    packer_old = json.loads(f.read())

packer_new = copy.deepcopy(packer_old)

if args.managed_image_name and args.managed_image_resource_group_name:
    # Delete VHD settings
    del packer_new["variables"]["resource_group"]
    del packer_new["variables"]["storage_account"]
    del packer_new["variables"]["capture_name_prefix"]
    del packer_new["builders"][0]["resource_group_name"]
    del packer_new["builders"][0]["storage_account"]
    del packer_new["builders"][0]["capture_container_name"]
    del packer_new["builders"][0]["capture_name_prefix"]
    # Insert managed image settings
    packer_new["variables"]["managed_image_name"] = args.managed_image_name
    packer_new["variables"][
        "managed_image_resource_group_name"] = args.managed_image_resource_group_name
    packer_new["builders"][0][
        "managed_image_name"] = '{{user `managed_image_name`}}'
    packer_new["builders"][0][
        "managed_image_resource_group_name"] = '{{user `managed_image_resource_group_name`}}'

    with open(packer_json, "w") as f:
        f.write(json.dumps(packer_new, sort_keys=False, indent=4))
else:
    if not args.shared_image_gallery:
        raise Exception("{} and/or {} arguments are missing".format(
            "--managed-image-name", "--managed-image-resource-group-name"))

if args.shared_image_gallery:
    # Insert managed image gallery settings
    with open("shared_image_gallery.json", "r") as f:
        shared_image_gallery_settings = json.loads(f.read())

    if 'managed_image_name' not in packer_new[
            "variables"] or 'managed_image_resource_group_name' not in packer_new[
                "variables"]:
        raise Exception('Managed image configuration is missing from template')

    packer_new["builders"][0][
        "shared_image_gallery_destination"] = shared_image_gallery_settings

    with open(packer_json, "w") as f:
        f.write(json.dumps(packer_new, sort_keys=False, indent=4))
