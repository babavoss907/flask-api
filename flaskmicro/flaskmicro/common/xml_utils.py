import logging
from lxml import etree as xmllib
from os import getenv

from jivacore.utils.xml_tools import XMLUtil
from correspondence.database import sessionLocal
from jivabase.refcode.db.sql.config_xml_search import ConfigXmlSearcher

logger = logging.getLogger('letters')


class ServiceXMLUtil:
    """
    """
    @classmethod
    def get_xml_data(cls, xml_cd):
        """
        """
        db_session = sessionLocal()
        searcher = ConfigXmlSearcher(db_session)
        searcher.get_config_xml_details()
        searcher.where_config_xml_entity_active()
        searcher.where_config_xml_cd(xml_cd=xml_cd)
        result = searcher.all()
        return result[0]

    @classmethod
    def get_root_element(cls, xml_data):
        try:
            root = xmllib.ElementTree(XMLUtil.parse_string(xml_data.xml_data)).getroot()
            return root
        except Exception as err:
            print("ERROR %s" % (err))
            logger.exception("Error in Fetching XML Data")
            raise Exception(err)

    @classmethod
    def get_config_value_dict(cls, section, xml_name='environment_options'):
        """
        """
        environ = getenv('Environment', 'LOCAL')
        result = cls.get_xml_data(xml_cd=xml_name)
        root = cls.get_root_element(xml_data=result)
        data_element = root.find(environ).find(section)
        config_items = {}
        for item in data_element.iterchildren():
            if item.attrib['enabled'] == 'Y':
                val = item.text.strip()
                kname = item.attrib['keyname']
                config_items[kname] = val
        return config_items

    @classmethod
    def get_configuration_status(cls, tag_name, xml_name='jivaConfigurables'):
        """
        def get_configuration_status_from_file(cls, tag_name, xml_cd='jivaConfigurables'):
        """
        try:
            if tag_name:
                result = cls.get_xml_data(xml_name)
                itemconf = XMLUtil.parse_string(result.xml_data).find(tag_name)
                if itemconf is not None:
                    isenabled = itemconf.xpath('@enabled')
                    if isenabled and isenabled[0] == 'Y':
                        if itemconf.text:
                            return itemconf.text
                        return True
            return False
        except Exception as e:
            print("Error %s " %(e))
            raise Exception("Error in fetching XML data")
        return False

    @classmethod
    def get_config_value(cls, section, option):
        """
        """
        environ = getenv('Environment', 'LOCAL')
        result = cls.get_xml_data('environment_options')
        root = cls.get_root_element(result)
        data_element = root.find(environ).find(section)
        if data_element is not None:
            for item in data_element.iterchildren():
                if str(item.attrib['keyname']) == option and str(item.attrib['enabled']) == 'Y':
                    result = item.text.strip()
        return result

    @classmethod
    def get_jiva_label(cls, element_name='', default_label=''):
        """
        """
        if not element_name and default_label:
            return default_label
        result = cls.get_xml_data(xml_cd='jivaLabel')
        if element_name or default_label:
            try:
                xml_data = xmllib.ElementTree(XMLUtil.parse_string(result.xml_data)).getroot().find(element_name)
                return str(xml_data.text)
            except Exception:
                if default_label:
                    return default_label
                else:
                    return element_name
        else:
            jiva_label_dict = {}
            lblxml = XMLUtil.parse_string(result.xml_data)
            lblobj = lblxml.xpath('./*')
            for label in lblobj:
                jiva_label_dict[str(label.tag)] = str(label.text)
            return jiva_label_dict

    @classmethod
    def get_pp_header_result(cls, db_session, context):
        """
        """
        result = cls.get_xml_data(xml_cd='ppDashboardConfig')
        jivacustom = XMLUtil.parse_string(result.xml_data)
        temp = []
        for each_child in jivacustom.iterchildren("*"):
            if each_child.tag == context:
                for each_sub_child in each_child:
                    if each_sub_child.attrib["show"] == "Y":
                        config_dict = {}
                        # replacing headers with jlabels
                        header_value = each_sub_child.attrib['header']
                        header_value = header_value.replace(
                            'Member', cls.get_jiva_label(element_name='patient', default_label='Patient'))
                        header_value = header_value.replace(
                            'Episode', cls.get_jiva_label(element_name='encounter', default_label='Episode'))
                        header_value = header_value.replace(
                            'Cert Number', cls.get_jiva_label(element_name='cert_number', default_label='Cert Number'))
                        header_value = header_value.replace(
                            'Status', cls.get_jiva_label(element_name='status', default_label='Status'))
                        each_sub_child.attrib['header'] = header_value
                        config_dict[
                            each_sub_child.tag] = dict(
                            each_sub_child.attrib)
                        config_dict[
                            each_sub_child.tag]["show"] = "true"
                        temp.append(config_dict)
        return temp

    @classmethod
    def get_config_value_dict(cls, section):
        """
        """
        environ = getenv('Environment', 'LOCAL')
        result = cls.get_xml_data('environment_options')
        root = cls.get_root_element(result)
        data_element = root.find(environ).find(section)
        config_items = {}
        for item in data_element.iterchildren():
            if item.attrib['enabled'] == 'Y':
                val = item.text.strip()
                kname = item.attrib['keyname']
                config_items[kname] = val
        return config_items

    @classmethod
    def get_xml_by_name(cls, xml_name, xml_tag=None):
        xml_data = cls.get_xml_data(xml_name)
        root = cls.get_root_element(xml_data)
        if xml_tag is not None:
            xml_root = root.find(xml_tag)
        return xml_root

    @classmethod
    def get_nurse_roles(cls, ce_enc_level=False):
        """
        @return : Returns the list of roles that are mapped as Nurse Roles
        """
        sroles = cls.get_configuration_status('subroles_of_tcm', 'userConfig')
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
            additional_tcm_roles = cls.get_configuration_status('additional_tcm_roles')
            if additional_tcm_roles:
                roles = str(additional_tcm_roles).split(',')
                tcm_roles.extend(roles)
        return tcm_roles

    @classmethod
    def get_element(cls, xml_tag):
        result = cls.get_xml_data(xml_tag)
        root = cls.get_root_element(result)
        return root

    @classmethod
    def get_xml_col_map_data(self, filename, xml_section_name, title_req=False):
        """
        This method returns xml tag values in list of dictionaries format
        @param filename : xml file name
        @param xml_section_name : xml section tag name
        """
        xml_section = ServiceXMLUtil.get_element(filename)
        header_list = []
        title_lst = []
        for each_child in xml_section.getroot().iterchildren("*"):
            if each_child.tag == xml_section_name:
                for each_sub_child in each_child:
                    if each_sub_child.attrib["enabled"] == 'Y':
                        temp = {each_sub_child.tag: dict(each_sub_child.attrib)}
                        header_list.append(temp)
                        title_lst.append(each_sub_child.attrib.keys())
        if title_req:
            return header_list, title_lst
        return header_list

    @classmethod
    def get_xml_col_map_data_two_leavel(self, filename, xml_section_name, req_tag):
        """
        This method returns xml tag values in list of dictionaries format
        @param filename : xml file name
        @param xml_section_name : xml section tag name
        """
        config = {}
        col_header = []
        xml_section = ServiceXMLUtil.get_element(filename)
        for each_child in xml_section.getroot().iterchildren("*"):
            if each_child.tag == xml_section_name:
                for each_sub_child in each_child:
                    if each_sub_child.tag == req_tag:
                        for child_tag in each_sub_child:
                            item_list = child_tag.getchildren()
                            tag_value = ''
                            tag_value = [item_child.text for item_child in item_list if item_child.tag == 'pdf']
                            if tag_value:
                                tag_value = tag_value[0]
                                if tag_value:
                                    config[child_tag.attrib.get('col')] = tag_value
                                    col_name = child_tag.attrib.get('col')
                                    col_header.append(col_name)
        return config, col_header

    @classmethod
    def get_xml_config_status(self, file_name, tag_name):
        """
        Method used to get enabled status of mapping table and other xml configurations used for ltss
        from ltssServiceConfig xml.

        Args:
            tag_name(string): xml tag name.

        Returns:
            enabled status as 0/1 or any values present in the tag.
        """
        xml_obj = ServiceXMLUtil.get_element(file_name).find(tag_name)
        if xml_obj is not None:
            is_enabled = xml_obj.xpath('@enabled')
            if is_enabled and is_enabled[0] == 'Y':
                if xml_obj.text:
                    return xml_obj.text
                return 1
        return 0
