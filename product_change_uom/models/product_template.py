# -*- coding: utf-8 -*-
# Copyright (C) DEC SARL, Inc - All Rights Reserved.
# Written by Yann Papouin <y.papouin at dec-industrie.com>, Jan 2021

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.addons.product.models import product_template
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def write(self, vals):
        if 'uom_id' in vals:
            new_uom = self.env['uom.uom'].browse(vals['uom_id'])
            updated = self.filtered(lambda template: template.uom_id != new_uom)
            product_variant_ids = updated.with_context(
                active_test=False
            ).mapped('product_variant_ids')
            active_moves = self.env['stock.move'].search(
                [
                    ('state', 'not in', ['cancel', 'done']),
                    ('product_id', 'in', product_variant_ids.ids)
                ],
                limit=1
            )
            if active_moves:
                raise UserError(
                    _(
                        "You cannot change the unit of measure as there "
                        "are active stock moves for this product. If you "
                        "want to change the unit of measure, you should "
                        "cancel/finish all of them or archive this product "
                        "and create a new one."
                    )
                )
            else:
                new_uom_id = self.env['uom.uom'].browse(vals['uom_id'])
                invalid_uoms = self.filtered(
                    lambda x: x.uom_id.category_id != new_uom.category_id
                ).mapped('uom_id.name')
                if invalid_uoms:
                    raise UserError(
                        _(
                            "UoM conversion from %s to %s is not possible "
                            "as they both belong to different Category!"
                        ) % (
                            ','.join(invalid_uoms),
                            new_uom_id.name,
                        )
                    )
                self._propagate_uom_change(new_uom_id)
                uom_vals = {'uom_id': vals.pop('uom_id')}
                # call super using original ProductTemplate to avoid built-in
                # uom_id change check
                super(product_template.ProductTemplate, self).write(uom_vals)
        res = super().write(vals)
        return res

    @api.multi
    def _propagate_uom_change(self, uom_id):
        """ We need to update quantity for all records with UoM related to
        the product one. Use regEx: related='.*.uom_id'
        Following model needs update:
            'product.packaging'
            'stock.quant'
            'stock.warehouse.orderpoint'
        Following model don't needs update:
            'stock.production.lot': quantity depends on 'stock.quant'
        Note, for uom_po_id:
        'product.supplierinfo'

        Args:
            uom_id ([uom.uom]): New UoM that will replace current one
        """
        product_ids = self.with_context(active_test=False)\
            .mapped('product_variant_ids')
        self._propagate_uom_change_to_quants(uom_id, product_ids)
        self._propagate_uom_change_to_orderpoints(uom_id, product_ids)
        self._propagate_uom_change_to_packagings(uom_id, product_ids)

    @api.multi
    def _propagate_uom_change_to_quants(self, uom_id, product_ids):
        """Convert quants quantities

        Args:
            uom_id ([uom.uom]): Future UoM that will replace current one
            product_ids ([product.product]): Source recordset
        """
        quant_ids = self.sudo().env['stock.quant'].search(
            [('product_id', 'in', product_ids.ids)]
        )
        for quant in quant_ids:
            current_uom_id = quant.product_id.uom_id
            quant.quantity = current_uom_id._compute_quantity(
                quant.quantity, uom_id
            )
            quant.reserved_quantity = current_uom_id._compute_quantity(
                quant.reserved_quantity, uom_id
            )

    @api.multi
    def _propagate_uom_change_to_orderpoints(self, uom_id, product_ids):
        """Convert orderpoints quantities

        Args:
            uom_id ([uom.uom]): Future UoM that will replace current one
            product_ids ([product.product]): Source recordset
        """
        orderpoint_ids = self.env['stock.warehouse.orderpoint'].search(
            [('product_id', 'in', product_ids.ids)]
        )
        for orderpoint in orderpoint_ids:
            current_uom_id = orderpoint.product_id.uom_id
            orderpoint.product_min_qty = current_uom_id._compute_quantity(
                orderpoint.product_min_qty, uom_id
            )
            orderpoint.product_max_qty = current_uom_id._compute_quantity(
                orderpoint.product_max_qty, uom_id
            )

    @api.multi
    def _propagate_uom_change_to_packagings(self, uom_id, product_ids):
        """Convert packaging quantities

        Args:
            uom_id ([uom.uom]): Future UoM that will replace current one
            product_ids ([product.product]): Source recordset
        """
        packaging_ids = self.env['product.packaging'].search(
            [('product_id', 'in', product_ids.ids)]
        )
        for packaging in packaging_ids:
            current_uom_id = packaging.product_id.uom_id
            packaging.qty = current_uom_id._compute_quantity(
                packaging.qty, uom_id
            )