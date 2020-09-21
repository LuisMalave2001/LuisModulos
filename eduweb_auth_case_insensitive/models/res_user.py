# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @classmethod
    def _login(cls, db, login, password):
        """ We lower the login variable """
        if login:
            login = login.lower()
        return super()._login(db, login, password)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["login"] = vals.get("login", "").lower()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("login"):
            vals["login"] = vals["login"].lower()
        return super().write(vals)
