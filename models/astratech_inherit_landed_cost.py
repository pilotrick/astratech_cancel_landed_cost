# -*- coding: utf-8 -*-

from odoo import models, fields, _


class astratechStockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'
    _description = 'Stock Landed Cost'

    def button_cancel(self):
        if self.account_move_id:
            self.account_move_id.button_cancel()
        
        related_move_ids = self.valuation_adjustment_lines.mapped('move_id')
        for record in related_move_ids:
            stock_valuation_layer_id = record.stock_valuation_layer_ids.filtered(lambda line: not line.stock_landed_cost_id)
            for line in stock_valuation_layer_id.stock_valuation_layer_ids:
                stock_valuation_layer_id.remaining_value -= line.value
                line.value = 0
        self.valuation_adjustment_lines.unlink()
        return self.write({'state': 'cancel', 'account_move_id':False})

    def action_set_to_draft(self):
        self.write({
            'state':'draft'
            })
