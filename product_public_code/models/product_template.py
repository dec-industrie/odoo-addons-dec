# -*- coding: utf-8 -*-
# Copyright (C) DEC SARL, Inc - All Rights Reserved.
# Written by Yann Papouin <y.papouin at dec-industrie.com>, Mar 2020

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    public_code = fields.Char(
        'Public Code',
        size=24,
        oldname="ciel_code",
    )

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        # If name starts with a wilcard, then clear arg domain
        if name.startswith('*'):
            name = name[1:]
            args = False
        if not args:
            args = []
        # Make a search with default criteria
        result = super().name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        result = self.append_extra_search(name, result, limit)
        return result

    @api.model
    def append_extra_search(self, name, name_search_result, limit=100):
        result = self.append_public_code_search(name, name_search_result, limit)
        return result

    @api.model
    def append_public_code_search(self, name, name_search_result, limit=100):
        result = name_search_result
        if name:
            # Make a specific search according to public code
            products = self.search(
                [
                    ('public_code', 'ilike', name + '%'),
                    '|',
                    ('state', '!=', 'obsolete'),
                    ('state', '=', False),
                ],
                limit=limit
            )
            if products:
                res = []
                for product in products:
                    item = list(product.name_get()[0])
                    item[1] = ('%s (%s)') % (item[1], product.public_code)
                    res.append(item)
                result = res + result
        return result