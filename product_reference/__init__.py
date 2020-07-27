from . import models
from . import wizard

from odoo import api, SUPERUSER_ID


def set_mrp_production_request(env):
    for ref in env['ref.reference'].search([]):
        ref.product_id.mrp_production_request = True


def post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    set_mrp_production_request(env)
