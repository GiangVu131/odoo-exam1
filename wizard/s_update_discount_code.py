from odoo import fields, models, api


class SPopupDiscountCode(models.TransientModel):
    _name = 's.update.discount.code'
    _description = 'Update discount code'
    input_customer_discount_code = fields.Text(string='Update Code')

    def _get_default_partner_ids(self):
        partner_ids = self.env.context.get('active_ids')
        if len(partner_ids) > 0:
            # for rec in self:
            #     # rec.partner_ids == [(6, 0, partner_ids)]
            return [(6, 0, partner_ids)]

    order_ids = fields.Many2many('sale.order', string='Customer Discount', default=_get_default_partner_ids)

    def mass_update_discount_code(self):
        self.ensure_one()
        for re in self.order_ids:
            re.customer_discount_code_so = self.input_customer_discount_code
