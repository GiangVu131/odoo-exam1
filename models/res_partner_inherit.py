from odoo import api, models, fields


class ResInherit(models.Model):
    _inherit = 'res.partner'
    customer_discount_code = fields.Text(string='Discount Code', store=True, compute='_compute_discount_value')
    active_discount_code = fields.Boolean(string='Active Code', default=False)
    number_value = fields.Integer(string='number', compute='_compute_number_value')
    sale_order_discount_estimated = fields.Char(string='Discount estimated', compute='_percent')

    @api.depends('active_discount_code', 'number_value')
    def _compute_discount_value(self):
        number = 'VIP_'
        for r in self:
            if not r.active_discount_code:
                r.customer_discount_code = ''
            else:
                r.customer_discount_code = number + str(r.number_value)

    @api.depends('active_discount_code', 'customer_discount_code')
    def _compute_number_value(self):
        number = True
        for r in self:
            if r.active_discount_code is False or not r.customer_discount_code:
                number = False
                r.number_value = 0
            else:
                number = True
        if number is True:
            self.number_value = int((self.customer_discount_code)[4:])
