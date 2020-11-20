from collections import namedtuple
import xmlrpc.client

XmlAccess = namedtuple("XmlAccess", "models db uid password")


def odoo_api_login(url, db, user, password):
    """
    :param url:  the url to the odoo instance, ex davinciderivatives.odoo.com
    :param db: name of the database to connect, can be retrieved in the user settings
    :param user: username to connect
    :param password: password or the api key
    """
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, user, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    return XmlAccess(models, db, uid, password)

def write_note_to_the_applicant(xml_access, applicant_id, subject, message):

    message_content = {
        'add_sign': True,
        'body': message,
        'message_type': 'email',
        'model': 'hr.applicant',
        'no_auto_thread': False,
        'res_id': applicant_id,
        'subject': subject,
        'subtype_id': 1
    }
    xml_access.models.execute_kw(xml_access.db, xml_access.uid, xml_access.password,
                      'mail.message', 'create',
                      [ message_content])

def update_applicant_stage(xml_access, applicant_id, stage_id):
    xml_access.models.execute_kw(xml_access.db, xml_access.uid, xml_access.password,
                                 'hr.applicant', 'write', [[applicant_id], {'stage_id' : stage_id}])
                                 

def refuse_candidate(xml_access, applicant_id, refuse_reason):
    xml_access.models.execute_kw(xml_access.db, xml_access.uid, xml_access.password,
                                 'hr.applicant', 'write', [[applicant_id], {'active' : False,
                                                                            'refuse_reason_id' : refuse_reason}])