from dataclasses import fields
from enum import UNIQUE

from requests import options
from zope.interface.common import optional

from odoo import models,fields
from odoo.addons.test_convert.tests.test_env import field
from odoo.release import description


class PropertyTag(models.Model):
    _name = "property.tags"
    _description='property tags'
    _rec_name = 'tag'
    _sql_constraints = [('Unique_tag','UNIQUE(tag)',"tag name must be unique")]
    _order = 'tag'

    tag = fields.Char('Tag',required=True)
    color=fields.Integer(string="color")