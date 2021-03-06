# -*- coding: utf-8 -*-
# Copyright (C) DEC SARL, Inc - All Rights Reserved.
# Written by Yann Papouin <y.papouin at dec-industrie.com>, Mar 2021

from odoo import api, fields, models


class SoftwareLicenseHardware(models.Model):
    _name = 'software.license.hardware'
    _description = 'License Hardware'
    _order = 'id desc'

    license_id = fields.Many2one(
        'software.license',
        'License',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(
        required=True,
        string="Identifier",
    )
    info = fields.Text('Informations')
