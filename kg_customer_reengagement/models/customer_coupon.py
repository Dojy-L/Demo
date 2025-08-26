from datetime import timedelta

from odoo import models, fields
import random
import string

def generate_coupon_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class CustomerCoupon(models.Model):
    _name = 'customer.coupon'
    _description = 'Customer Coupon'

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    code = fields.Char(required=True, readonly=True)
    is_used = fields.Boolean(default=False)
    expiration_date = fields.Datetime()

    @classmethod
    def generate_coupon(cls, env, partner):
        code = generate_coupon_code()

        coupon = env['customer.coupon'].create({
            'partner_id': partner.id,
            'code': code,
            'expiration_date': fields.Datetime.now() + timedelta(days=30),
        })
        print(f"Generated coupon code '{code}' for partner '{partner.name}' (ID: {partner.id})")
        return coupon.code
