from odoo import fields, models, api


class SPopupDiscountCode(models.TransientModel):
    _name = 's.update.discount.code'
    _description = 'Update discount code'
    input_numbers = fields.Integer(string='')

    def _get_default_partner_ids(self):
        partner_ids = self.env.context.get('active_ids')
        if len(partner_ids) > 0:
            # for rec in self:
            #     # rec.partner_ids == [(6, 0, partner_ids)]
            return [(6, 0, partner_ids)]

    partner_ids = fields.Many2many('res.partner', string='Customer Discount', default=_get_default_partner_ids)

    def mass_update_discount_code(self):
        self.ensure_one()
        for re in self.partner_ids:
            re.discount_value = re.discount_value + self.input_numbers
