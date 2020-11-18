$(window).on('load', page_changed);

function page_changed(event)
    {
    frappe.after_ajax(function () 
        {
            var route = frappe.get_route();
            if(route[0] == "pos")
            {
                var button_off = document.createElement('button');
                button_off.style.color = "white";
                button_off.innerHTML = 'Add Coupon';
                let container = document.querySelector('div.col-sm-12');
                container.appendChild(button_off).style.backgroundColor = "#5e64ff";
                button_off.onclick = function()
                {
                    d.show();
                }
            }
            else if(route[0]=="point-of-sale")
            {
                var button_off = document.createElement('button');
                button_off.style.color = "white";
                button_off.innerHTML = 'Add Coupon';
                let container = document.querySelector('div.clearfix');
                //container.innerHTML  = container.innerHTML + "<br/>" ;
                container.appendChild(button_off).style.backgroundColor = "#5e64ff";
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

    net_total_text = document.querySelector('div.net-total').textContent // extracting net total value
    net_total_int = net_total_text.match(/\d+/)[0] //extracting integer values from net-total array as string
    net_total = parseInt(net_total_int) // converting string to integer
    
    frappe.call({
        method: "erpnext_pos_coupon.codex.get_value",
        args: 
        {
            "field_name":val.coupon_code, 
            net_total:net_total
        },
        callback: function(r){
            var k = JSON.parse(r.message)
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
                var discount = document.querySelector('input.discount_amount');
                discount.value = k.discount_value
            }
            else if (k.discount_type == "Percentage")
            {
                var discount = document.querySelector('input.additional_discount_percentage');
                discount.value = k.discount_value
            }
            discount.dispatchEvent(new Event('change'));     
        }
    }); 
        d.hide();
    }
});
