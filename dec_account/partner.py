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

from osv import fields, osv
from tools.translate import _


class res_partner(osv.osv):
    """
    Extends the partners to add a payment terms for purchases option.
    """
    _inherit = 'res.partner'

    _columns = {
        'property_payment_term_supplier': fields.property(
            'account.payment.term',
            type='many2one',
            relation='account.payment.term',
            string ='Payment Term',
            method=True,
            view_load=True,
            help="This payment term will be used instead of the default one for the current partner on purchases"),
    }
    
res_partner()

    