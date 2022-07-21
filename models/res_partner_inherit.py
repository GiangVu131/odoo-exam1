from odoo import api, models, fields


class ResInherit(models.Model):
    _inherit = 'res.partner'
    discount_value = fields.Integer('Discount Value', compute='_compute_discount_value', store=True,
                                    readonly=False)
    valid_code = fields.Char(compute='_compute_valid_code', string='Valid Code', store=True)
    sale_order_discount_estimated = fields.Char(string='Discount estimated', compute='_percent')
    active_discount_code = fields.Boolean(string='Active Code', default=False)
    Sale_order_discount_estimated = fields.Monetary(string='Discount Estimated')

    @api.depends('active_discount_code')
    def _compute_discount_value(self):
        for r in self:
            if not r.active_discount_code:
                r.discount_value = 0

    @api.depends('active_discount_code', 'discount_value')
    def _compute_valid_code(self):
        for r in self:
            if r.active_discount_code is False or not r.discount_value:
                r.valid_code = 0
            else:
                r.valid_code = 'VIP_' + str(r.discount_value)[0:3]

    @api.depends('discount_value', 'active_discount_code')
    def _percent(self):
        for r in self:
            if r.active_discount_code is False or not r.discount_value:
                r.sale_order_discount_estimated = 0
            else:
                r.sale_order_discount_estimated = str(r.discount_value)[0:3] + '%'

    @api.constrains('discount_value')
    def _check_discount_value(self):
        for r in self:
            if r.discount_value > 100:
                raise models.ValidationError('Discount value must be < 100')
            elif r.discount_value < 0:
                raise models.ValidationError('Discount value must be > 0')

    _sql_constraints = [
        (
            'check_name', "CHECK( (type='contact' AND name IS NULL) or (type!='contact') )",
            'Contacts require a name'),
    ]
