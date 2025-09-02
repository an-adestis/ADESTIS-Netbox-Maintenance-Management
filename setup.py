from setuptools import find_packages, setup

setup(
    name='adestis-netbox-maintenance-management',
    version='1.0.0',
    description='ADESTIS Maintenance Management',
    # url='https://github.com/adestis/netbox-account-management',
    author='ADESTIS GmbH',
    author_email='pypi@adestis.de',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    keywords=['netbox', 'netbox-plugin', 'plugin'],
    package_data={
        "adestis_netbox_maintenance_management": ["**/*.html"],
        '': ['LICENSE'],
    }
)