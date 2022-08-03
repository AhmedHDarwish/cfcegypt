# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Salesperson Own Customers",
    
    "author": "Softhealer Technologies",
    
    "website": "https://www.softhealer.com",
        
    "version": "13.0.3",
    
    "category": "Sales",
    
    "summary": """
salesperson specific customer, vendor see particular customer, special customer module odoo, seller get particular client""",        
    "description": """Currently in odoo all customers are visible to salesperson, For this our module will help to show only specific customers to salesperson.""",
     
    "depends": ['sale_management','base'],
    
    "data": [
        'views/users.xml',
        'views/sales_person_orders.xml',
    ],    
    
    "images": ["static/description/background.png",],
                 
    "installable": True,
    "auto_install": False,
    "application": True,  
      
    "price": "19",
    "currency": "EUR"          
}
