from odoo import fields, models, api


class SPopupWarranty(models.TransientModel):
    _name = 's.update.warranty'
    _description = 'Update Warranty'
    input_date_from = fields.Date(string='Change Date Start')
    input_date_to = fields.Date(string='Change Date End')
    date_from_update = fields.Date(related='product_ids.date_from', string='Date Start')
    date_to_update = fields.Date(related='product_ids.date_to', string='Date End')

    def _get_default_product_ids(self):
        product_ids = self.env.context.get('active_ids')
        if len(product_ids) > 0:
            return [(6, 0, product_ids)]

    product_ids = fields.Many2many('product.template', string='Warranty', default=_get_default_product_ids)

    def mass_update_warranty(self):
        self.ensure_one()
        for r in self.product_ids:
            r.date_from = self.input_date_from
            r.date_to = self.input_date_to
