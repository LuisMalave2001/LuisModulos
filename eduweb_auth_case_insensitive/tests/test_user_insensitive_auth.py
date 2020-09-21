# -*- coding: utf-8 -*-

from odoo import tests, api, registry
from odoo.tools import mute_logger


class TestUserInsensitiveAuth(tests.common.TransactionCase):
    def setUp(self):
        super(TestUserInsensitiveAuth, self).setUp()
        self.login = 'EmailFoo@boO.Com'
        self.partner_vals = {
            # "name": "Partner",
            "is_company": False,
            "email": self.login,
        }
        self.vals = {
            # "name": "User",
            "login": self.login,
            "password": "password",
        }
        self.model_obj = self.env["res.users"]

    def _new_test_user(self):
        """ Just create a new object to test it """
        partner_id = self.env["res.partner"].create(self.partner_vals)
        # self.vals["partner_id"] = partner_id.id
        return self.model_obj.create(self.vals)

    def test_login_is_lowercased_on_create(self):
        """ Login should be lowercased on create method """
        user_id = self._new_test_user()
        self.assertEquals(user_id.login, self.login.lower(), "Login was not lowercased when saved to db.")

    def test_login_is_lowercased_on_write(self):
        """ Login should be lowercased on write method """
        user_id = self._new_test_user()
        user_id.write({"login": self.login})
        self.assertEqual(user_id.login, self.login.lower(), "Login was not lowercased when saved to db.")

    @mute_logger("odoo.addons.auth_ldap.models.res_company_ldap")
    def test_login_login_is_lowercased(self):
        """ It should verify the login is set to lowercase on login """
        rec_id = self._new_test_user()

        # We have to commit this cursor, because `_login` uses a fresh cursor
        self.env.cr.commit()
        res_id = self.model_obj._login(
            self.env.registry.db_name, self.login.upper(), "password"
        )

        # Now clean up our mess to preserve idempotence
        # with api.Environment.manage():
        with registry(self.env.registry.db_name).cursor() as new_cr:
            new_cr.execute("DELETE FROM res_users WHERE login='%s'" % self.login.lower())
            new_cr.commit()

        self.assertEqual(
            rec_id.id,
            res_id,
            "Login with with uppercase chars was not successful",
        )
