from attr import fields

from odoo import models, fields, api


class SalesOrdersLineInherit(models.Model):
    _inherit = 'sale.order.line'
    sale_order_discount_estimated_sol = fields.Char(related='order_id.sale_order_discount_estimated_so',
                                                    string='Customer Discount')

    number_value_so = fields.Integer(related='order_id.number_value_so')
    price_total_discount = fields.Monetary(compute='_compute_discount', string='Price Subtotal')
    warranty_estimated_so = fields.Char(related='product_id.sale_order_discount_estimated_pt', string='Product Discount')
    product_warranty_so = fields.Text(string='', related='product_id.product_warranty')
    warranty_discount_total_so = fields.Float(string='', compute='_compute_warranty_discount_total')
    numbers_percent = fields.Char(compute='_compute_numbers_percent', string='Customer discount')

    @api.depends('number_value_so')
    def _compute_numbers_percent(self):
        for rec in self:
            rec.numbers_percent = str(rec.number_value_so) + '%'

    @api.depends('price_subtotal', 'number_value_so')
    def _compute_discount(self):
        for r in self:
            r.price_total_discount = r.price_subtotal - ((r.price_subtotal * r.number_value_so) / 100)

    @api.depends('price_unit')
    def _compute_warranty_discount_total(self):
        for record in self:
            if not record.warranty_estimated_so:
                record.warranty_discount_total_so = record.price_unit
            else:
                record.warranty_discount_total_so = record.price_unit - ((record.price_unit * 10) / 100)

    @api.depends('product_uom_qty', 'discount', 'warranty_discount_total_so', 'tax_id')
    def _compute_amount(self):
        for line in self:
            price = line.warranty_discount_total_so * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
