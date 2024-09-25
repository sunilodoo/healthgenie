# -*- coding: utf-8 -*-

{
    "name" : "Custom Invoicing",
    # "version" : "1.0",
    "author" : "Santosh Singh",
    "description": """Custom Invoice""",
    "website" : "www.Healthgenie.in",
    "category" : "Account",
	"summary" : "Accounts",
    "depends": ['account'],
    "data" : [
		"security/ir.model.access.csv",
		"view/account_invoice_view.xml",
        "wizard/excel_report_view.xml",
        # 'report/invoice_report.xml',
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
