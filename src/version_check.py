import pkg_resources
from src import log


def check_version() -> None:
    # Setting up the logger
    logger = log.setup_logger(__name__)
    
    # Create a list to store the names and versions of packages with mismatched versions
    mismatched_packages = []
    
    # Open the requirements.txt file
    with open('requirements.txt') as f:
        # Read each line in the file
        for line in f:
            # Split the line into the package name and required version
            package_name, package_verion = line.strip().split('==')
            # Use pkg_resources to get information about the installed version of the package
            installed = pkg_resources.get_distribution(package_name)
            # Extract the package name and installed version
            name, version = installed.project_name, installed.version
            # Compare the installed version to the required version
            if line.strip() != f'{name}=={version}':
                # If the versions do not match, add the package to the list of mismatched packages
                mismatched_packages.append((name, version))
    
    # If there are any mismatched packages, log a summary of these packages
    if mismatched_packages:
        logger.error('The following packages have mismatched versions:')
        for name, version in mismatched_packages:
            logger.error(f'{name}: installed version {version} does not match the required version')