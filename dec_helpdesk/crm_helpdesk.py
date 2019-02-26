# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

import time

from osv import fields
from osv import osv
from tools.translate import _


class crm_helpdesk(osv.osv):
    _name = "crm.helpdesk"
    _inherit="crm.helpdesk"
    
    def _get_shop_id(self, cr, uid, ids, context=None):
        cmpny_id = self.pool.get('res.users')._get_company(cr, uid, context=context)
        shop = self.pool.get('sale.shop').search(cr, uid, [('company_id', '=', cmpny_id)])
        return shop and shop[0] or False
    
    _columns = {
        'partner_city': fields.related('partner_id', 'city', type='text', string='City'),
    }
    
    def make_sale_order(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        sale_obj = self.pool.get('sale.order')
        partner_obj = self.pool.get('res.partner')
        new_ids = []
        
        for case in self.browse(cr, uid, ids, context=context):
            partner = case.partner_id
            partner_addr = partner_obj.address_get(cr, uid, [partner.id], ['default', 'invoice', 'delivery', 'contact'])
            pricelist = partner.property_product_pricelist.id
            fpos = partner.property_account_position and partner.property_account_position.id or False

            if not partner and case.partner_id:
                partner = case.partner_id
                fpos = partner.property_account_position and partner.property_account_position.id or False
                partner_addr = partner_obj.address_get(cr, uid, [partner.id], ['default', 'invoice', 'delivery', 'contact'])
                pricelist = partner.property_product_pricelist.id
            if False in partner_addr.values():
                raise osv.except_osv(_('Data Insufficient!'), _('Customer has no addresses defined!'))

            vals = {
                'summary': _('SAV%05d: %s') % (case.id, case.name), 
                'origin': _('SAV%05d') % (case.id),
                'section_id': case.section_id and case.section_id.id or False,
                'categ_id': case.categ_id and case.categ_id.id or False,
                #'shop_id': self._get_shop_id.id,
                'partner_id': partner.id,
                'pricelist_id': pricelist,
                'partner_invoice_id': partner_addr['invoice'],
                'partner_order_id': partner_addr['contact'],
                'partner_shipping_id': partner_addr['delivery'],
                'date_order': fields.date.context_today(self,cr,uid,context=context),
                'fiscal_position': fpos,
            }
            if partner.id:
                vals['user_id'] = partner.user_id and partner.user_id.id or uid
            new_id = sale_obj.create(cr, uid, vals, context=context)
            sale_order = sale_obj.browse(cr, uid, new_id, context=context)
            self.write(cr, uid, [case.id], {'ref': 'sale.order,%s' % new_id})
            new_ids.append(new_id)
            message = _("Helpdesk case '%s' is converted to Quotation.") % (case.name)
            self.log(cr, uid, case.id, message)
            self.message_append(cr, uid, [case], _("Converted to Sales Quotation(%s).") % (sale_order.name), context=context)

            #if case.close:
            #    self.case_close(cr, uid, data)
        if not new_ids:
            return {'type': 'ir.actions.act_window_close'}
        if len(new_ids)<=1:
            value = {
                'domain': str([('id', 'in', new_ids)]),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sale.order',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'res_id': new_ids and new_ids[0]
            }
        else:
            value = {
                'domain': str([('id', 'in', new_ids)]),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'res_id': new_ids
            }
        return value
    

crm_helpdesk()
