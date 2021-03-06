# Author: Damien Crier
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    property_subcontracted_service = fields.Boolean(
        compute="_compute_property_subcontracted_service",
    )

    @api.depends('service_to_purchase')
    def _compute_property_subcontracted_service(self):
        for rec in self:
            rec.property_subcontracted_service = rec.service_to_purchase
