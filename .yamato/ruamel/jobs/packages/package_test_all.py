from ruamel.yaml.scalarstring import DoubleQuotedScalarString as dss
from ..shared.namer import packages_filepath, package_job_id_test_all, package_job_id_test, package_job_id_test_dependencies
from ..shared.yml_job import YMLJob
from ..shared.constants import NPM_UPMCI_INSTALL_URL


class Package_AllPackageCiJob():
    
    def __init__(self, packages, agent, platforms, target_editor, target_branch, editor):
        self.job_id = package_job_id_test_all(editor["track"])
        self.yml = self.get_job_definition(packages, agent, platforms, target_editor, target_branch, editor).get_yml()


    def get_job_definition(self, packages, agent, platforms, target_editor, target_branch, editor):

        # define dependencies
        dependencies = []
        for platform in platforms:
            for package in packages:
                dependencies.append(f'{packages_filepath()}#{package_job_id_test(package["id"],platform["os"],editor["track"])}')
                #dependencies.append(f'{packages_filepath()}#{package_job_id_test_dependencies(package["id"],platform["os"],editor["track"])}')
        
        # construct job
        job = YMLJob()
        job.set_name(f'Pack and test all packages - { editor["track"] } [package context]')
        job.set_agent(agent)
        job.add_dependencies(dependencies)
        job.add_var_custom_revision(editor["track"])
        job.add_commands([
                f'npm install upm-ci-utils@stable -g --registry {NPM_UPMCI_INSTALL_URL}',
                f'upm-ci package izon -t',
                f'upm-ci package izon -d'])
        # if editor['track'] == f'fast-{target_editor}':
        #     # trigger the job when updating the docs to avoid merging jpg images (this is not allowed by the package validation suite)
        #     job.set_trigger_on_expression(f'pull_request.target eq "{target_branch}" AND NOT pull_request.draft AND pull_request.push.changes.any match ["**/Documentation*/**/*"]')
        return job
        
    