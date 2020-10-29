$(window).on('load', page_changed);

function page_changed(event)
    {
    frappe.after_ajax(function () 
        {
            var route = frappe.get_route();
            if(route[0] == "pos")
            {
                var button_off = document.createElement('button');
                button_off.innerHTML = 'Add Coupon Offline';
                let container = document.querySelector('div.col-sm-12');
                container.innerHTML  = container.innerHTML + "<br/>" ;
                container.appendChild(button_off);
                button_off.onclick = function()
                {
                    d.show();
                }
            }
        })
    }


let d = new frappe.ui.Dialog({
    title: 'Enter details',
    fields: [
        {
            label: 'Coupon Code',
            fieldname: 'coupon_code',
            fieldtype: 'Data'
        }
        
    ],
    primary_action_label: 'Apply',
    primary_action(val) {
    frappe.call({
        method: "erpnext_pos_coupon.codex.get_value",
        args: {"field_name":val.coupon_code },
        callback: function(r){
            var k = JSON.parse(r.message)
            if (r.message == "null")
            {
                frappe.throw('Invalid Coupon Code')
            }
            else
            {
                if (k.coupon_type == "Gift Card")
                {
                    var customer_ = document.querySelector("input[data-fieldname='customer']");
                    if(customer_.value != k.customer)    
                    {
                        frappe.throw("You do not have this Offer")
                        return false
                    }
                }
                if (k.discount_type == "Amount")
                {
                    var discount = document.querySelector('input.discount-amount');
                    discount.value = k.discount_value
                }
                else if (k.discount_type == "Percentage")
                {
                    var discount = document.querySelector('input.discount-percentage');
                    discount.value = k.discount_value
                }
                discount.dispatchEvent(new Event('change'));     
            }
        }
    }); 
        d.hide();
    }
});