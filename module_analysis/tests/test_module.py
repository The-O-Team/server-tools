# Copyright (C) 2019-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.modules.module import get_module_path
from odoo.tests.common import TransactionCase, at_install, post_install


@at_install(False)
@post_install(True)
class TestModule(TransactionCase):

    def setUp(self):
        super().setUp()
        self.IrModuleModule = self.env['ir.module.module']

    def test_installed_modules(self):
        self.IrModuleModule.cron_analyse_code()
        installed_modules = self.IrModuleModule.search(
            [('state', '=', 'installed')])
        for module in installed_modules:
            module_path = get_module_path(module.name)
            if "site-packages" in module_path:
                # Addon is installed as a Python package.
                # Individual files may not be available for analysis.
                continue
            self.assertTrue(
                module.python_code_qty > 0 or
                module.xml_code_qty > 0 or
                module.js_code_qty > 0,
                "module '%s' doesn't have code analysed defined, whereas it is"
                " installed." % (module.name))

    def test_uninstalled_modules(self):
        uninstalled_modules = self.IrModuleModule.search(
            [('state', '!=', 'installed')])
        for module in uninstalled_modules:
            self.assertTrue(
                module.python_code_qty == 0,
                "module '%s' has python lines defined, whereas it is"
                " not installed." % (module.name))
