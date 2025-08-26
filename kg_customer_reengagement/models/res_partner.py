from odoo import models, fields
from datetime import timedelta


class ResPartner(models.Model):
    _inherit = 'res.partner'

    inactive_customer = fields.Boolean(string='Inactive Customer', default=False, readonly=True)

    def _compute_inactive_customers(self):
        param = self.env['ir.config_parameter'].sudo()
        days = int(param.get_param('kg_customer_reengagement.inactive_days'))
        print("daysdays",days)
        if days:
            limit_date = fields.Datetime.now() - timedelta(days=days)
            SaleOrder = self.env['sale.order']

            active_partner_ids = SaleOrder.search([
                ('date_order', '>=', limit_date),
                ('state', 'in', ['sale', 'done'])
            ]).mapped('partner_id').ids
            print("Active customers:", active_partner_ids)

            all_customers = self.search([])

            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

            for partner in all_customers:
                print("partner", partner)
                is_inactive = partner.id not in active_partner_ids
                partner.inactive_customer = is_inactive

                if is_inactive:
                    coupon_code = self.env['customer.coupon'].generate_coupon(self.env, partner)
                    print(f"Coupon: {coupon_code} for partner {partner.name}")


                    recent_order = partner.sale_order_ids.sorted('date_order', reverse=True)[:1]
                    portal_url = recent_order.get_portal_url() if recent_order else f"{base_url}/shop"

                    mail_values = {
                        'subject': f'Customer Re-Engagement {partner.name}',
                        'body_html': f"""
                            <p>Dear {partner.name},</p>
                            <p>We noticed you haven't shopped with us in a while. We'd like to have you back!</p>
                            <p>Here's a 10% discount — use this code at checkout: <strong>{coupon_code}</strong></p>
                            <p><strong>Your Discount Code:</strong> {coupon_code}</p>
                            <p>
                                <a href="{portal_url}" style="padding:10px 15px;background:#007BFF;color:#fff;text-decoration:none;border-radius:5px;">
                                    Shop Now
                                </a>
                            </p>
                            <p>Hope to see you soon!<br/>Your Company Team</p>
                        """,
                        'email_to': partner.email,
                        'email_from': partner.company_id.email or 'yourcompany@example.com',
                    }
                    self.env['mail.mail'].create(mail_values).send()

