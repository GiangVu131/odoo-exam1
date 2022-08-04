from odoo import models, fields, api


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    date_from = fields.Date('Date Start')
    product_warranty = fields.Text('Product Warranty', compute='_compute_product_warranty')
    sale_order_discount_estimated_pt = fields.Char(compute='_compute_sale_order_discount_estimated_pt', string='Warranty Discount')
    date_to = fields.Date('Date End')
    warranty_left = fields.Char(string='Days Warranty Left', compute='_compute_warranty_left')
    list_price = fields.Monetary('List Price')

    @api.depends('list_price', 'sale_order_discount_estimated')
    def _compute_warranty_discount_total(self):
        for r in self:
            r.warranty_discount_total = r.list_price - r.sale_order_discount_estimated

    @api.depends('date_to')
    def _compute_warranty_left(self):
        for r in self:
            if r.date_to:
                currentDate = fields.Date.today()
                deadlineDate = fields.Datetime.to_datetime(r.date_to).date()
                daysLeft = deadlineDate - currentDate
                years = ((daysLeft.total_seconds()) / (365.242 * 24 * 3600))
                yearsInt = int(years)
                months = (years - yearsInt) * 12
                monthsInt = int(months)
                days = (months - monthsInt) * (365.242 / 12)
                daysInt = int(days)
                r.warranty_left = '{0:d} years ,' \
                                  ' {1:d}  months ,' \
                                  ' {2:d}  days ' \
                    .format(yearsInt, monthsInt, daysInt)
                if yearsInt < 0 or monthsInt < 0 or daysInt < 0:
                    r.warranty_left = 'Out of warranty'
                else:
                    pass
            else:
                r.warranty_left = 'No warranty'

    @api.depends('date_to', 'date_from')
    def _compute_sale_order_discount_estimated_pt(self):
        for r in self:
            if r.date_to and r.date_to < fields.Date.today():
                r.sale_order_discount_estimated_pt = '10%'
            elif r.date_to is True and r.date_from is True:
                r.sale_order_discount_estimated_pt = ''
            elif r.date_to is False and r.date_from is False:
                r.sale_order_discount_estimated_pt = '10%'
            else:
                r.sale_order_discount_estimated_pt = ''

    @api.depends('date_to', 'date_from')
    def _compute_product_warranty(self):
        for r in self:
            if r.date_to is False and r.date_from is False:
                r.product_warranty = 'No Warranty'
            else:
                r.product_warranty = 'PWR/' + str(r.date_from)[5:7] + str(r.date_from)[8:10] + str(r.date_from)[
                                                                                               2:4] + '/' + str(
                    r.date_to)[5:7] + str(r.date_to)[8:10] + str(r.date_to)[2:4]

    @api.constrains('date_from', 'date_to')
    def _check_date(self):
        for r in self:
            if not r.date_from and r.date_to:
                raise models.ValidationError('Must have Date Start')
            elif not r.date_to and r.date_from:
                raise models.ValidationError('Must have Date End')
            elif r.date_from > r.date_to:
                raise models.ValidationError('Date End must be > Date Start')
