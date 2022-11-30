import sys
import logging
from sqlalchemy import func, and_

from jivacore.db.base_entity import db
from jivacore.utils.xml_tools import XMLUtil
from jivabase.message.db.message_ent import CodeMessage
from jivacore.utils.xml_utils import JivaXMLUtil
from jivabase.user.model.user_common_model import UserCommonModel
from .constants import PROVIDER_ROLES


logger = logging.getLogger(__name__)


def get_xml_data(db_session, xml_cd):
    searcher = ConfigXmlSearcher(db_session)
    searcher.get_config_xml_details()
    searcher.where_config_xml_entity_active()
    searcher.where_config_xml_cd(xml_cd=xml_cd)
    return searcher.all()[0]


def get_loggedin_user_idn(db_session, sys_user_id):
    """
    To fetch the user_idn value for the sys_user_id.
    Args:
        session (obj): Database session obj
        sys_user_id (str): login user name
    Return:
        user_idn (int): user idn value
    """
    try:
        result = db_session.query(db.SysUser.user_idn)\
            .filter(and_(db.SysUser.sys_user_id == sys_user_id,
                         db.SysUser.sysusr_active == 'Y')).one()
        return result.user_idn
    except Exception as err:
        return int(2)  # Revisit to fix this user_idn value


def get_loggedin_user_roles(db_session, username=''):
    """
    def get_logged_in_user_roles()
    This function is to fetch the user roles for the username.
    Args:
        session (obj): Database session obj
        username (str): login user name
    Returns:
        user_roles (tuple): user roles
    """
    user_roles = db_session.query(db.UserRole.user_type_id).filter(
        db.UserRole.sys_user_id == username).all()
    return user_roles


def get_query_content_for_wildchar_search(query):
    """
    @param query: query content
    @return: This method will return query content for % like searches of code values in POC

    taken from getQueryContentForWildCharSearch from ZeAutoCompleteCtrl.py
    """
    prefix_required = 'No'
    if query == '%':
        # re_exp = "[$!@#^*()`~;:<>?/,_\"]"
        query = ''
        prefix_required = 'Yes'
    if query != '%' and query.startswith('%'):
        # re_exp = "[$!@#^*()`~;:<>?/,_\"]"
        query = query[1:]
        prefix_required = 'Yes'
    return query, prefix_required


def add_wildchar(request, key):
    """ Add wild character '%' prefix and suffix of the given value """
    request = request.args.to_dict()
    if key in request:
        tmp1 = str(request[key]).lower()
        tmp = tmp1.strip()
        if tmp != '' and tmp.find('*') == -1:
            tmp = '%' + tmp + '%'
            request[key] = tmp
        elif tmp.find('*') != -1:
            tmp = tmp.replace('*', '%')
            request[key] = tmp
    return request


def get_default_record_per_page(tag_name='defaultRecordPerPage'):
    """
    """
    try:
        rec_per_page = JivaXMLUtil.get_configuration_status(tag_name=tag_name)
        return int(rec_per_page)
    except Exception:
        return 10


def get_jiva_message(db_session, msg_type='CONFIRMATION', msg_code=None):
    """
    """
    if msg_code:
        result_msg_code = ''
        if JivaXMLUtil.get_config_value('GENERAL', 'show_message_code'):
            result_msg_code = "( " + msg_code + ")"
        msg = get_msg_from_db(msg_type, msg_code, db_session)
        if msg:
            # if message is not fetched from ZeCache query DB to get message details
            # msg = self.ZeUI.getMsgFromDB(msg_code, msg_type)
            dup_msg = msg.split('DMSG_ID_')
            if len(dup_msg) > 1:
                msg = get_msg_from_db(msg_type, dup_msg[1], db_session)
        if msg:
            return parse_jivalabel(db_session, msg)
        return msg
    else:
        return "Invalid message code"


def check_duplicate_message(msg, db_session):
    """
    checking if message description is having duplicate message id to process
    """
    dup_msg = msg.split('DMSG_ID_')
    if len(dup_msg) > 1:
        msg = get_code_msg_details(msg, dup_msg[1], db_session)
        if not msg:
            msg = get_msg_from_db(msg, dup_msg[1], db_session)
    return msg


def parse_jivalabel(session, msg):
    """
    Parse a given string againsed Jiva lable configured in xml
    """
    existing_lables = JivaXMLUtil.get_jiva_label()
    restult_message = msg
    for itm in existing_lables.keys():
        restult_message = restult_message.replace(itm, existing_lables[itm])
    return restult_message


def get_code_msg_details(msg_type, msg_code, session):
    """
    """
    if not JivaXMLUtil.get_configuration_status(tag_name='isJivaMsgsCacheEnabled'):
        return None
    return get_msg_descriptiion(session, msg_type, msg_code)


def get_msg_from_db(msg_type, msg_code, session):
    """
    """
    msg_desc = session.query(CodeMessage.description).filter(
        and_(CodeMessage.message_cd == msg_code, CodeMessage.message_type == msg_type)).first()

    if msg_desc and msg_desc[0]:
        msg = msg_desc[0]
        msg = convert_to_jlabel_msg(msg)
        return msg
    else:
        msg = "Invalid " + msg_type + " Message Code : " + msg_code
        logger.info(msg, 200)
        raise KeyError(msg)


def convert_to_jlabel_msg(mesgs):
    """
    # convertToJlabelMsg
    This method is used to convert to jlabel depending
    on the message text whether it is episode/member.

    Args:
        mesgs (str): Messages to be converted to jlabel

    Returns:
        str: Returns the message after converting
    """
    if mesgs.__contains__('$episode'):
        mesgs = ' '.join(
            [JivaXMLUtil.get_jiva_label(element_name='encounter', default_label='Encounter') if '$' in i else i for i in
             mesgs.split()])
    elif mesgs.__contains__('$member'):
        mesgs = ' '.join(
            [JivaXMLUtil.get_jiva_label(element_name='patient', default_label='Patient') if '$' in i else i for i in
             mesgs.split()])
    return mesgs


def get_msg_descriptiion(session, msg_type, msg_code):
    """
    Fetch the message descfiption for the combination of msg_type and msg_cdoe.
    Args:
        session (obj): Database session object
        msg_type (str): message type
        msg_code (str): message code
    Returns:
        Result set
    """
    result = session.query(CodeMessage.description).filter(and_(CodeMessage.message_cd == msg_code,
                                                                CodeMessage.message_type == msg_type))
    first = result.first()
    return first[0] if first else first


def normalize_form(exclusionids=()):  # pragma: no cover
    """
    Decorator function used to scrub unwanted html from form-submitted data.

    Typically this is used as a decorator for controller methods.

    Optional parameter `exclusionids` is a tuple of Ids which need no
    scrubbing. TODO Why not?
    """
    def decorator(func):
        def wrappedfunc(self, *args, **kwargs):
            """ """
            REQUEST = self.REQUEST
            global_exclusion_ids = get_global_exclusion_ids(exclusionids)
            interested_ids = filter(lambda element_id: element_id not in global_exclusion_ids, REQUEST.form.keys())
            for obj in interested_ids:
                val = ''
                objval = REQUEST.form[obj]
                if isinstance(objval, str) and objval:
                    try:
                        val = bleach.clean(objval,
                                           tags=ALLOWED_TAGS,
                                           attributes=ALLOWED_ATTRIBUTES,
                                           strip=True)
                        val = val.replace('&amp;', '&')
                        val = val.encode('ascii', 'ignore')
                        REQUEST.form[obj] = val
                    except Exception:
                        REQUEST.form[obj] = objval
            REQUEST.form = REQUEST.form.copy()
            REQUEST.form['normalizer_info'] = 'Normalize Decorator'
            return_func = func(self, *args, **kwargs)
            return return_func
        return wrappedfunc
    return decorator


def get_global_exclusion_ids(exclusionids):
    """
    To get the all exclusion ids
    """
    global_exclusion_ids = ['I_ENCOUNTER_IDN', 'I_CLAIMANT_IDN', 'I_ENC_TYPE_CD', 'cwqiresponse']
    if exclusionids:
        if isinstance(exclusionids, str):
            global_exclusion_ids.append(exclusionids)
        else:
            global_exclusion_ids.extend(list(exclusionids))
    return global_exclusion_ids


def get_notification_checks(obj):
    """
    getNotificationChecks
    """
    check_list = []
    try:
        result = JivaXMLUtil.get_xml_data('notificationChecks')
        root = XMLUtil.parse_string(result.xml_data).find(obj)
        for ele in root.findall('Check'):
            if ele.find('Show').text == 'Y':
                chk_lst_label = ele.find('Label').text
                chk_lst_label = chk_lst_label.replace('Patient', JivaXMLUtil.get_jiva_label(
                    element_name='patient', default_label='Patient'))
                chk_lst_label = chk_lst_label.replace('Client', JivaXMLUtil.get_jiva_label(
                    element_name='payor', default_label='Payor'))
                check_list.append({'LABEL': chk_lst_label, 'VALUE': ele.find('Value').text})
    except Exception:
        return check_list
    return check_list


def get_notification_config_details(config_key=''):
    """
    def getNotificationConfigDetails()
    This function is used to get the value of notification configuration.
    If config_key is present then return the value of it or the all notification_config
    Args:
        config_key (str): configuration key
    Return:
        note_conf (dict): notification configurations
    """
    note_conf = {}
    result = JivaXMLUtil.get_xml_data(xml_cd='notificationConfig')
    root = XMLUtil.parse_string(result.xml_data).find('CONSTANTVALUES')
    for record in root:
        kname = record.attrib['keyname']
        val = record.text
        note_conf[kname] = val
    if config_key:
        return note_conf[config_key]
    return note_conf

def get_configured_episodes_and_user_roles(db_session):
        """
        This Method is to get episode configured for PP and NP, and logged in user roles.
        """
        prv_enc_types = ''
        user_roles = get_loggedin_user_roles(db_session, username='AUTHENTICATED_USER')
        episodes_configured = JivaXMLUtil.get_configuration_status('encounters')
        if is_provider_portal(db_session):
            prv_enc_types = JivaXMLUtil.get_configuration_status('enc_types_show_pp')
        return user_roles, episodes_configured, prv_enc_types

def is_provider_portal(db_session):
    """ Returns 1(True) if Provider Portal Login else 0(False)
        This method is used in Ze_lookup.js, Ze_jiva.js and expects 1 or 0 """
    user_roles = get_loggedin_user_roles(db_session)
    if set(PROVIDER_ROLES).isdisjoint(set(user_roles)):
        return 0
    return 1


def get_exception_message():
    """
    """
    templist = ()
    try:
        templist = (str(sys.exc_type), str(sys.exc_value),
                    'Line No: ' + str(sys.exc_traceback.tb_lineno))
    except Exception as err:
        logger.error(err)
    return templist


def get_nurse_roles(ce_enc_level=False):
    """
    @return : Returns the list of roles that are mapped as Nurse Roles
    """
    sroles = JivaXMLUtil.get_configuration_status('subroles_of_tcm', 'userConfig')
    tcm_roles = []
    if sroles:
        for t in str(sroles).split(','):
            tcm_roles.append(t + 'MANAGER')
            tcm_roles.append(t + 'READER')
    # is_crm = self.ZeUI.isCRMLogin()
    is_crm = ['TCM']
    if is_crm:
        tcm_roles.append('QAR')

    if ce_enc_level:
        additional_tcm_roles = JivaXMLUtil.get_configuration_status('additional_tcm_roles')
        if additional_tcm_roles:
            roles = str(additional_tcm_roles).split(',')
            tcm_roles.extend(roles)
    return tcm_roles
