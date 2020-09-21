# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LowerCaseAllUserLogins(models.TransientModel):
    _name = "lower.case.all.user.logins"

    @api.model
    def lower_case_all_user_logins(self):
        user_ids = self.env["res.users"].sudo().search([])
        for user_id in user_ids:
            user_id.login = user_id.login.lower()