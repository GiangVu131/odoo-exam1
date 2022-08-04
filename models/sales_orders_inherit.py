from odoo import api, models, fields
import json


class SalesOrdersInherit(models.Model):
    _inherit = 'sale.order'

    customer_discount_code_so = fields.Text(string='Valid Code', related='partner_id.customer_discount_code',
                                            store=True)
    active_discount_code_so = fields.Boolean(related='partner_id.active_discount_code', string='Active Code')
    sale_order_discount_estimated_so = fields.Char(string='Discount Estimated',
                                                   related='partner_id.sale_order_discount_estimated')
    number_value_so = fields.Integer(related='partner_id.number_value')

    amount_untaxed = fields.Monetary(compute='_amount_all_123')
    tax_totals_json = fields.Char(compute='_compute_tax_totals_json')

    @api.depends('order_line.price_total_discount')
    def _amount_all_123(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_total_discount
                amount_tax += line.price_tax
            order.update({
                'amount_total': amount_untaxed + amount_tax,
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
            })

    @api.depends('order_line.tax_id', 'order_line.warranty_discount_total_so', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):
        def compute_taxes(order_line):
            price = order_line.warranty_discount_total_so * (1 - (order_line.discount or 0.0) / 100.0)
            order = order_line.order_id
            return order_line.tax_id._origin.compute_all(price, order.currency_id, order_line.product_uom_qty,
                                                         product=order_line.product_id,
                                                         partner=order.partner_shipping_id)

        account_move = self.env['account.move']
        for order in self:
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line,
                                                                                         compute_taxes)
            tax_totals_1 = account_move._get_tax_totals(order.partner_id,
                                                        tax_lines_data,
                                                        order.amount_untaxed,
                                                        order.amount_total,
                                                        order.currency_id,
                                                        )
            tax_totals_2 = account_move._get_tax_totals(order.partner_id,
                                                        tax_lines_data,
                                                        order.amount_total,
                                                        order.amount_untaxed,
                                                        order.currency_id,
                                                        )
            order.tax_totals_json = json.dumps(tax_totals_1)
            order.tax_totals_json = json.dumps(tax_totals_2)
