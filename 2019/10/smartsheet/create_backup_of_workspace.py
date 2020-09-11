"""

"""
from datetime import datetime

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import smartsheet
import logging

from smartsheet.folders import Folders
from smartsheet.models import ContainerDestination, Workspace, Folder
from smartsheet.sheets import Sheets
from smartsheet.sights import Sights
from smartsheet.workspaces import Workspaces

ACCESS_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
SENDGRID_API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'

logger = logging.getLogger('create_backup_of_workspace')
hdlr = logging.FileHandler('./create_backup_of_workspace.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

OPTIONAL_ELEMENTS_TO_INCLUDE = ['attachments', 'cellLinks', 'data', 'discussions', 'filters', 'forms',
                                'ruleRecipients', 'rules']


def create_backup_of_workspace(workspace_id, email_address_to_notify):
    """ This is the main function, the one you want to run.  The other functions should have their names start with
    underscores to indicate that they're not meant to be run directly by the user of the program.

    :param workspace_id: int
    :return:
    """
    smart = smartsheet.Smartsheet(ACCESS_TOKEN)

    workspaces = Workspaces(smart)

    original_workspace = workspaces.get_workspace(workspace_id, load_all=True)

    try:
        number_of_objects_in_workspace = _get_number_of_objects_in_workspace_or_folder_including_subfolders(original_workspace)

        print("Original workspace:")
        _pretty_print_subfolders_and_object_counts(original_workspace)

        backup_workspace_name = 'BACKUP_%s_%s' % (datetime.today().strftime('%d%m%y'), original_workspace.name)
        if number_of_objects_in_workspace < 100:
            response = workspaces.copy_workspace(workspace_id,
                                                 smartsheet.models.ContainerDestination({
                                                     'new_name': backup_workspace_name
                                                 }),
                                                 include=OPTIONAL_ELEMENTS_TO_INCLUDE)
        else:
            backup_workspace = Workspace({
                'name': backup_workspace_name
            })
            response = workspaces.create_workspace(backup_workspace)
            logger.log(logging.INFO, response)
            backup_workspace.id = response.data.id
            _copy_objects_from_workspace_or_folder(smart, original_workspace, backup_workspace)
            _copy_subfolders(smart, original_workspace.folders, backup_workspace)

            _verify_the_result(workspaces, original_workspace, backup_workspace)
        _send_success_email(email_address_to_notify, original_workspace.name)
    except Exception as e:
        _send_failure_email(email_address_to_notify, original_workspace.name,
                            error_message=repr(e))


def _get_number_of_objects_in_workspace_or_folder_including_subfolders(workspace_or_folder):
    """ The purpose of this function is to determine whether a specified workspace or folder has hit the 100-object
    limit that indicates that it cannot be copied in one go with the 'copy_workspace()' or 'copy_folder()' commands.

    :param workspace_or_folder: Workspace or Folder object
    :return:
    """
    total_number_of_objects = _get_number_of_objects_in_folder_excluding_subfolders(workspace_or_folder)

    folders_to_check = [folder for folder in workspace_or_folder.folders]

    while folders_to_check:
        current_folder = folders_to_check.pop()
        total_number_of_objects += _get_number_of_objects_in_workspace_or_folder_including_subfolders(current_folder)

    return total_number_of_objects


def _get_number_of_objects_in_folder_excluding_subfolders(folder, exclude_uncopyable_objects=False):
    """ This function is used by several other functions.

    I added the 'exclude_uncopyable_objects' parameter after I discovered that the 'templates' and 'reports'
    objects do not seem to have a way to be copied individually (e.g. 'copy_template()'), which is a problem when I
    am trying to copy a folder that contains more than 100 objects (where that number includes objects in subfolders)
    *and* contains templates/reports *directly* beneath it (i.e. not in a subfolder), because the process for copying
    the workspace in that case is to 1) create a new workspace, 2) copy the individual objects from the original
    workspace into the new workspace, and 2) copy the subfolders over.  But if some of the individual objects can't be
    copied over (i.e. templates and reports), then a *full* copy of the original workspace is not possible. To verify
    that the original workspace was properly copied, it thus becomes necessary to be able to count the number
    of objects in the original workspace that *can* be copied given this limitation of the API.

    :param folder: Folder object
    :param exclude_uncopyable_objects: bool
    :return:
    """
    total = len(folder.sheets) + len(folder.sights)
    if not exclude_uncopyable_objects:
        total += len(folder.templates) + len(folder.reports)
    return total


def _pretty_print_subfolders_and_object_counts(folder, indent=0):
    """ This function will display the structure of folders and their number of objects in a similar way to the web UI.
    I created this function while trying to troubleshoot problems in this program because I didn't have access to the
    web UI.

    :param folder: Folder object
    :param indent: int
    :return:
    """
    for folder in folder.folders:
        number_of_objects = _get_number_of_objects_in_folder_excluding_subfolders(folder)
        output_string = '%s: %d' % (folder.name, number_of_objects)
        print('\t' * indent + str(output_string))
        _pretty_print_subfolders_and_object_counts(folder, indent + 1)


def _copy_objects_from_workspace_or_folder(smart, original_workspace_or_folder, backup_workspace_or_folder):
    """ This function copies *only* the objects *at the level of* the specified workspace or folder.  It does *not* copy
    objects from subfolders.

    :param smart: Smartsheet object
    :param original_workspace_or_folder: Workspace or Folder object
    :param backup_workspace_or_folder: Workspace or Folder object
    :return:
    """
    sheets_operations_object = Sheets(smart)
    for sheet in original_workspace_or_folder.sheets:
        response = sheets_operations_object.copy_sheet(sheet.id_,
            ContainerDestination({
                'destination_type': 'workspace' if type(original_workspace_or_folder) == Workspace else 'folder',
                'destination_id': backup_workspace_or_folder.id_,
                'new_name': sheet.name
            }), include=OPTIONAL_ELEMENTS_TO_INCLUDE)
        logger.log(logging.INFO, response)

    sights_operations_object = Sights(smart)
    for sight in original_workspace_or_folder.sights:
        response = sights_operations_object.copy_sight(sight.id_,
            ContainerDestination({
                'destination_type': 'workspace' if type(backup_workspace_or_folder) == Workspace else 'folder',
                'destination_id': backup_workspace_or_folder.id_,
                'new_name': sight.name
            }))
        logger.log(logging.INFO, response)


def _copy_subfolders(smart, folders_to_copy, backup_containing_workspace_or_folder):
    """

    :param smart: Smartsheet object
    :param folders_to_copy: list of Folder objects
    :param backup_containing_workspace_or_folder: Workspace or Folder object
    :return:
    """
    for original_subfolder in folders_to_copy:
        number_of_objects_in_this_folder = _get_number_of_objects_in_workspace_or_folder_including_subfolders(original_subfolder)
        if number_of_objects_in_this_folder < 100:
            _copy_folder_immediately(smart, original_subfolder, backup_containing_workspace_or_folder)
        else:
            new_folder = Folder({
                'name': original_subfolder.name
            })
            folders_operations_object = Folders(smart)
            response = folders_operations_object.create_folder_in_folder(backup_containing_workspace_or_folder.id, new_folder)
            logger.log(logging.INFO, response)
            new_folder.id = response.data.id
            _copy_objects_from_workspace_or_folder(smart, original_subfolder, new_folder)
            _copy_subfolders(smart, original_subfolder.folders, new_folder)


def _copy_folder_immediately(smart, folder, destination):
    """ This function will copy a folder and all of its subfolders and all of their objects.  It should only be used on
    folders that contain less than 100 objects (where that number includes objects in subfolders).

    :param smart: Smartsheet object
    :param folder: Folder object
    :param destination: Folder object
    :return:
    """
    folders_operations_object = Folders(smart)
    response = folders_operations_object.copy_folder(folder.id_,
                                                     ContainerDestination({
                                                         'destination_type': 'workspace' if type(destination) == Workspace else 'folder',
                                                         'destination_id': destination.id_,
                                                         'new_name': folder.name
                                                     }),
                                                     include=OPTIONAL_ELEMENTS_TO_INCLUDE)
    logger.log(logging.INFO, response)


def _verify_the_result(workspaces, original_workspace, backup_workspace):
    """ This function contains some code I wrote while trying to resolve problems in the program, and it seemed helpful
    enough to be worth keeping around after the problems were resolved.

    :param workspaces:
    :param original_workspace:
    :param backup_workspace:
    :return:
    """
    number_of_copyable_objects_in_original_workspace = _get_number_of_copyable_objects_in_workspace_or_folder(
        original_workspace)
    backup_workspace = workspaces.get_workspace(backup_workspace.id, load_all=True)
    number_of_objects_in_new_workspace = _get_number_of_objects_in_workspace_or_folder_including_subfolders(
        backup_workspace)

    logger.log(logging.INFO,
               'number_of_copyable_objects_in_original_workspace: %d' % number_of_copyable_objects_in_original_workspace)
    logger.log(logging.INFO, 'number_of_objects_in_new_workspace: %d' % number_of_objects_in_new_workspace)

    print("Backup workspace:")
    _pretty_print_subfolders_and_object_counts(backup_workspace)

    assert number_of_objects_in_new_workspace == number_of_copyable_objects_in_original_workspace


def _get_number_of_copyable_objects_in_workspace_or_folder(workspace_or_folder):
    """ This function is basically the same idea as '_get_number_of_objects_in_workspace_or_folder_including_subfolders()',
    with one exception: if a folder contains more than 100 objects (with that number including any objects in subfolders),
    then there seems to be no way of copying over that folder's templates and reports.  So if we want to make sure the
    original workspace was properly copied by comparing the number of objects from the old and the new workspace, we
    need to use this function to only count the objects from the original workspace that will actually be copyable. Note
    that any *sub*folders that contain fewer than 100 objects *will* have templates and reports copied over.

    :param workspace_or_folder: Workspace or Folder object
    :return:
    """
    number_of_objects_in_folder = _get_number_of_objects_in_workspace_or_folder_including_subfolders(workspace_or_folder)
    if number_of_objects_in_folder >= 100:
        number_of_objects_in_folder = _get_number_of_objects_in_folder_excluding_subfolders(workspace_or_folder, exclude_uncopyable_objects=True)
        for folder in workspace_or_folder.folders:
            number_of_objects_in_folder += _get_number_of_copyable_objects_in_workspace_or_folder(folder)
    return number_of_objects_in_folder


def _send_success_email(recipient_email_address, original_workspace_name):
    email_subject = 'Workspace \'%s\' has been copied' % original_workspace_name
    email_contents = email_subject
    _send_result_email(recipient_email_address, email_subject, email_contents)


def _send_failure_email(recipient_email_address, original_workspace_name,
                          error_message):
    email_subject = 'Error copying workspace \'%s\'' % original_workspace_name
    email_contents = error_message
    _send_result_email(recipient_email_address, email_subject, email_contents)


def _send_result_email(recipient_email_address, email_subject, email_contents):
    _send_email("XXXXXXXXXXXXXXXXXXXXXXXXXXX",
                to_email_address=recipient_email_address,
                subject=email_subject,
                content=email_contents,
                content_type="text/html")


def _send_email(from_email_address, to_email_address=None, subject=None, content=None,
                 content_type="text/plain"):
    """

    :param from_email_address: string of the email address, eg 'noreply@asdf.com'
    :param to_email_address: string of the email address, eg 'joekale@gmail.com'
    :param subject:
    :param content:
    :param content_type:
    :return:
    """
    message = Mail(
        from_email=from_email_address,
        to_emails=to_email_address,
        subject=subject,
        html_content=content)
    sg = SendGridAPIClient(SENDGRID_API_TOKEN)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)


if __name__ == '__main__':
    create_backup_of_workspace(111111111111111111,
                               email_address_to_notify='XXXXXXXXXXXXXXXXXXXXXXXXXXX')
