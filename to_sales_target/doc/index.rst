Installation
============

1. Navigate to Apps
2. Find with keyword 'to_sales_target'
3. Install it as usual then you are done.

Please note that:

1. If you have Sales application installed and the module `Sales Target Management - Sales Management` (technical name: `to_sales_target_sale`) available in your addons path, the `to_sales_target_sale` will also be installed automatically
2. If you have Points of Sales application installed and the module `Sales Target Management - Point of Sales` (technical name: `to_sales_target_pos`) available in your addons path, the `to_sales_target_pos` will also be installed automatically

Security
========

1. Thanks to the dependency on the module `to_sales_team_advanced`, your sales user groups will be organized as below
	* **Sales / User: Own Documents Only**:
		* view team of which she or he is a member
		* propose personal target for approval
	* **Sales / Sales Team Leader**:
		* view/edit team of which she or he is either a member or the team leader
		* propose team target for approval by Regional Managers
		* set and approve targets for team members	
	* **Sales / Regional Manager**:
		* view/edit/create/delete team of which she or he is either a member or the team leader or the regional manager
		* approve / reject targets for the teams under his hands
	* **Sales / User: All Documents**:
		* full access rights for all teams but sales configurations
	* **Sales / Manager**: Full access rights to Sales Management application, including doing configuration

Instructions
============

General Setup
-------------

1. Define sales target for your sales teams (also known as sales channel since Odoo v11):
	* !IMPORTTAN: You need to be a sales team leader or in a higher access group to do this task
	* Navigate to Sales Target > Team Sales Target
	* Create a new Draft Target by:
		* Select a team. All the team members will be loaded automatically into the Personal Sales Target table under.
		* Select a period for the target by input Start Date and End Date
		* Input your sales target (in your company currency) for the period specified above. Upon changing of the sales target amount, Odoo will automatically calculate the team members' target amount by equal division. For example, you set $100,000 for the team while the team has 10 members, Odoo will put $10,000 as sales target for each and every member of the team. However, this amount could be overriden by manual input
	* Confirm your team sales target
		* Hit confirm button to confirm the target. All the personal sales target of the team will be confirmed too.
		* Upon confirmation, the status of the team sales target will become "Waiting Approved".
		* An authorized user who have Regional Manager access rights and is assigned to manage the team will be able to approve and reject the target 
		
2. Define your own personal sales target. There are two ways to complete this task
	1. Do it with your Sales Team
		* Find your Sales Team to which you belong.
		* Open it in form view
		* Input your desired sales amount as your target
	2. Navigate to Sales Target > Personal Sales Target > My Sales Target
		* Find the target that your team leader created for you
		* Modify your target amount and confirm it

Tracking your targets and their reach
------------------------------------

Sales Target Management - Sales Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is required that the module `to_sales_target_sale` MUST be available and installed in your Odoo instance to have the following features

1. Track the sales teams' team targets and their reach:
	* Find the team you want to track then open it in form view
	* On the tab 'Personal Sales Target', you will find target reach (progress) of your team members
	* On the tab 'Sales KPI', you will find:
		* Sales Total: the total sales recorded by the Sales Management application for the period of the target
		* Target Reach: Ther percentage of the Sales Total vs. the Team Target
		* Invoiced Total: the total sales that have been invoiced during the period of the target

2. Track the personal sales targets and their reach
	* Navigate to Sales Target > Personal Sales Target > All Sales Targets
	* Switch between list view and pivot view and graph view to see all the aspects of personal sales targets
	
Sales Target Management - Point of Sales
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It is required that the module `to_sales_target_pos` MUST be available and installed in your Odoo instance to have the following features

1. Sales Total is now included sales recorded in both Point of Sales and Sales Management applications
2. Invoice Total is now included sales invoiced from both Point of Sales and Sales Management applications
3. On the 'Sales KPI' tab, you will find an additional block that shows you:
	* **Non-Invoiced PoS Sales Total**: the total sales recorded in Point of Sales but not invoiced during the period of the target.
	* **Invoiced PoS Sales Total**: the total sales recorded in Point of Sales that have been invoiced during the period of the target.
	* **PoS Sales Total**: Total sales recorded in Point of Sales during the period of the target. It should be equal to: `Non-Invoiced PoS Sales Total + Invoiced PoS Sales Total`
	* **Target Reached**: The percentage of the PoS Sales Total vs. Sales Target
