odoo.define('to_sales_target_management.sales_team_dashboard', function(require){
  "use strict";

  var core = require('web.core');
  var _t = core._t;
  
  var dashboard = require('sales_team.dashboard');

  dashboard.include({
	  on_dashboard_target_clicked: function(ev){
		  var $target = $(ev.currentTarget);
		  var target_name = $target.attr('name');
		  if (target_name == 'invoiced'){
			  this.do_warn(_t("Please ask your sales team leader to set your target this month in Sales Target application."));
			  return;
		  }
		  this._super(ev);
	  }
  });
    
});
