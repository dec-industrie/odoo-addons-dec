# -*- coding: utf-8 -*-
# Copyright (C) DEC SARL, Inc - All Rights Reserved.
# Written by Yann Papouin <y.papouin at dec-industrie.com>, Mar 2021

from Crypto.PublicKey import RSA
from odoo import api, fields, models


class SoftwareLicenseApplication(models.Model):
    _inherit = 'software.license.application'

    auto_generate_serial = fields.Boolean(
        string="Auto-generate Serial",
        help="Automatically generate a random pref-formatted serial when "
        "creating a new license for this application",
    )
