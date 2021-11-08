# Introduction
Aim of this repository is to provide sample Azure DevOps YAML pipelines to build VM images used by Azure DevOps MS Hosted agents.<br>
Github Actions and Azure DevOps MS Hosted agents are built from [actions/virtual-environments](https://github.com/actions/virtual-environments)<br>
YAML pipeline templates included in this repository are using above repository to build the same images in your private environment.<br>

Currently only building using Ubuntu MS Hosted agents has been tested.

# Getting Started
1.  Make sure you have at least one parallel job purchased for MS Hosted pipelines as MS Hosted agent will time out after 60 minutes.
    You can use public azure-devops project which does have a limit of 6 hours by default, however be aware that your build logs will be publicly available.
3.	Copy contents of this repository to your Azure Repo
4.	Create Github service connection [github-service-connection](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops&tabs=yaml#github-service-connection)
    You can create PAT token without any scopes to create github service conneciton which only has access to public information [creating-a-personal-access-token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
5.	Import one or more templates from [azure-pipelines/](azure-pipelines/)
6.	Replace `endpoint: <name of github service connection>` , `service_connection: <name of azure service connection>` and other settings with your values.
7.	Run the pipeline

# YAML templates
There is currently three examples of template for each of supported agents:
1. `-vhd-minimal.yml` - This template is using default packer template from [actions/virtual-environments](https://github.com/actions/virtual-environments) repository.
    - No modifications to packer template are being made
    - Requires `ARM_RESOURCE_GROUP` and `ARM_STORAGE_ACCOUNT` settings to be specified.
    - Packer will build an VHD image and store it in your azure storage account specified in `ARM_STORAGE_ACCOUNT`
    - NOTE: VHD packer images are being deprecated
    - Template example: [ubuntu-2004-vhd-minimal.yml](azure-pipelines/ubuntu-2004-vhd-minimal.yml)

2. `-managed-image.yml` - This template is using packer template from [actions/virtual-environments](https://github.com/actions/virtual-environments) repository.
    - Packer definition is modified by one of the tasks and use [misc/custom_config.py](misc/custom_config.py) to perform modifications.
    - Requires `managed_image_name` and `managed_image_resource_group_name` settings to be specified.
    - Packer will build managed image with specified name in resource group specified in `managed_image_resource_group_name` setting.
    - One of the steps will display packer template before and after modifications.
    - Modified packer template will be published alongside other artifacts for future reference.
    - Template example: [ubuntu-2004-managed-image.yml](azure-pipelines/ubuntu-2004-managed-image.yml)

3. `-managed-image-shared-image-gallery.yml` - This template is using packer template from [actions/virtual-environments](https://github.com/actions/virtual-environments) repository.
    - Packer definition is modified by one of the tasks and use [misc/custom_config.py](misc/custom_config.py) to perform modifications.
    - Requires `managed_image_name` and `managed_image_resource_group_name` settings to be specified.
    - Requires `shared_image_gallery_destination` settings to be specified [shared_image_gallery_destination](https://www.packer.io/docs/builders/azure/arm#shared_image_gallery_destination)
    - Packer will build managed image with specified name in resource group specified in `managed_image_resource_group_name` setting and publish the image to shared image gallery [shared-image-galleries](https://docs.microsoft.com/en-us/azure/virtual-machines/shared-image-galleries) (Now called Azure Compute Gallery)
    - One of the steps will display packer template before and after modifications.
    - Modified packer template will be published alongside other artifacts for future reference.
    - Template example: [ubuntu-2004-managed-image-shared-image-gallery.yml](azure-pipelines/ubuntu-2004-managed-image-shared-image-gallery.yml)

All of above templates are configured to automatically trigger when there is new release of given image at [actions/virtual-environments](https://github.com/actions/virtual-environments) repository.
To disable this delete trigger settings as shown below:
```yaml
    trigger:
      branches:
        include:
        - refs/heads/ubuntu20/*
```

There is also single template to build all images at once without automatic trigger located under [images-all-shared-image-gallery-matrix.yml](azure-pipelines/images-all-shared-image-gallery-matrix.yml)

# Troubleshooting:

If your build fails at packer build stage and worked previously check official Azure DevOps pipeline runs under [https://github.visualstudio.com/virtual-environments/_build](https://github.visualstudio.com/virtual-environments/_build).

In many cases official builds will fail due to various reasons. If it fails with the same error as you can see in your build please raise issue at [actions/virtual-environments](https://github.com/actions/virtual-environments) repository.
If you cannot see the same error there, raise issue in this repository.




### TODO:
- [ ] Add examples how to use with custom vnet
- [ ] Add and test ability to use self hosted agents for build process.
- [ ] Add more documentation/wiki
