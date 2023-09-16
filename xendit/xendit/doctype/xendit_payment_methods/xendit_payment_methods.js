// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Xendit Payment Methods', {
	refresh: function (frm) {
		if (frm.doc.fee_calculation && frm.doc.name){
			if (!cur_frm.is_new()){
				cur_frm.events.calculate_fee_example();
			}
		}
	},
	calculate_fee_example: function () {
		var html = `Fill the calculation above with math alogarithm. For an example: <br>
		<var>( total + 2000 ) * 1.2</var><b> or </b><var>( total ) * 1.2 </var><br> <b>or</b>
		<var>( ceil ((total * 0.01) / 1000.0) * 1000 )</var><br>
		And please to include <code> total(as a Grand Total) </code>
		`;
		
		frappe.call({
			method: "xendit.xendit.doctype.xendit_payment_methods.xendit_payment_methods.calculate",
			args: {
				'total': 10000,
				'xendit_payment_methods' : cur_frm.doc.name
			},
			callback: function (data) {
				console.log(data)
				html = " <b> This is example result with variable (total = 10.000) : </b>"+data.message.toString()+"<br>"+html;
				cur_frm.set_df_property("fee_example", "options", html);

			}
		});

		cur_frm.set_df_property("fee_example", "options", html);
	}

});