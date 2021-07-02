# -*- coding: utf-8 -*-
# Copyright (C) DEC SARL, Inc - All Rights Reserved.
# Written by Yann Papouin <y.papouin at dec-industrie.com>, May 2021

from odoo import _, fields, models


class SoftwareLicense(models.Model):
    _inherit = 'software.license'

    portal_published = fields.Boolean(
        'In Portal',
        related='application_id.portal_published',
        store=True,
    )

    def _prepare_hardware_activation_vals(self, hardware):
        res = super()._prepare_hardware_activation_vals(hardware)
        if res.get('dongle_identifier') > 0:
            res['validity_days'] = 365
        return res
