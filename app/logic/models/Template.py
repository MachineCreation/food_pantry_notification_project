#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/logic/models/Template.py
# Author: Joseph Egan
# 2026-05-17
# Sources:
# Contributors: Lloyd Truong
# -------------------------------------------------------------------------------
# Description: Class to handle and store Template objects for use in sending
# notifications

# Local imports
from app.database.models.Database import Database

# python imports
# from typing import List


class Template():

    __all_templates = {}

    def __init__(self,
                 template_id,
                 template_name,
                 creator_id,
                 subject,
                 template_body,
                 tags,
                 created_date,
                 image_path=None):
        self.__template_id = template_id
        self.__template_name = template_name
        self.__creator_id = creator_id
        self.__subject = subject
        self.__template_body = template_body
        self.__tags = tags
        self.__created_date = created_date
        self.__image_path = image_path

# ----------------------------------- properties ------------------------------
    @property
    def template_name(self):
        '''
        string name of template
        '''
        return self.__template_name
    
    @property
    def subject(self):
        '''
        string subject of template
        '''
        return self.__subject
    
    @property
    def template_body(self):
        '''
        string body of template
        '''
        return self.__template_body
    
    @property
    def tags(self):
        '''
        List of tag strings
        '''
        return self.__tags
    
    @property
    def template_id(self):
        '''
        int id of template
        '''
        return self.__template_id
    
    @property
    def creator_id(self):
        '''
        int id of user that created template
        '''
        return self.__creator_id
    
    @property
    def created_date(self):
        return self.__created_date

    @property
    def image_path(self):
        '''
        image path of template
        '''
        return self.__image_path

# --------------------------------- class methods -----------------------------
    @classmethod
    def get_all_templates(
            cls,
            database: Database
    ):
        '''
        retrieve all current templates and store them on the class for quick
        access
        '''
        templates_tuples = database.get_all_templates()

        for template in templates_tuples:
            cls.__all_templates[template[1]] = Template(*template)

    # --------------------
    @classmethod
    def all_templates(cls) -> dict:
        '''
        dict of template object references
            template_name: Template object
        '''
        return cls.__all_templates
