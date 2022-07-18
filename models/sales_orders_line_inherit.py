from attr import fields

from odoo import models, fields, api


class SalesOrdersLineInherit(models.Model):
    _inherit = 'sale.order.line'
    discount_estimated_used = fields.Char(related='order_id.discount_estimated', string='Customer Discount'
                                          )
    discount_value_relate_2 = fields.Integer(related='order_id.discount_value_relate_1', string='Number value'
                                             )
    price_total_discount = fields.Monetary(compute='_compute_discount', string='Price Subtotal')

    warranty_estimated_2 = fields.Char(related='product_id.warranty_estimated', string='Product Discount')
    warranty_discount_total_2 = fields.Float(string='', compute='_compute_warranty_discount_total')

    @api.depends('price_subtotal', 'discount_value_relate_2')
    def _compute_discount(self):
        for r in self:
            r.price_total_discount = r.price_subtotal - ((r.price_subtotal * r.discount_value_relate_2) / 100)

    @api.depends('price_unit', 'warranty_estimated_2')
    def _compute_warranty_discount_total(self):
        for record in self:
            if not record.warranty_estimated_2:
                record.warranty_discount_total_2 = record.price_unit
            else:
                record.warranty_discount_total_2 = record.price_unit - ((record.price_unit * 10) / 100)

    @api.depends('product_uom_qty', 'discount', 'warranty_discount_total_2', 'tax_id')
    def _compute_amount(self):
        for line in self:
            price = line.warranty_discount_total_2 * (1 - (line.discount or 0.0) / 100.0)
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
