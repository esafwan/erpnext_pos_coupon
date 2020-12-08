from __future__ import unicode_literals
import frappe
from frappe.utils import cint, cstr, getdate, today
from frappe import throw, _
from frappe.utils.nestedset import NestedSet, get_ancestors_of, get_descendants_of
import json 

def update_coupon_code_count(coupon_name,transaction_type):
    coupon=frappe.get_doc("Coupon Code",coupon_name)
    if coupon:
        if transaction_type=='used':
            if coupon.maximum_use:
                if coupon.used<coupon.maximum_use:
                    coupon.used=coupon.used+1
                    coupon.save(ignore_permissions=True)
                else:
                    frappe.throw(_("{0} Coupon used are {1}. Allowed quantity is exhausted").format(coupon.coupon_code,coupon.used))
	    # elif transaction_type=='cancelled':
		#     if coupon.used>0:
		# 	    coupon.used=coupon.used-1
		# 	    coupon.save(ignore_permissions=True)

def validate_coupon_code(coupon_name):
    coupon = frappe.get_doc("Coupon Code", coupon_name)
    if coupon.valid_from:
        if coupon.valid_from > getdate(today()):
            frappe.throw(_("Sorry, this coupon code's validity has not started"))
    if coupon.valid_upto:
        if coupon.valid_upto < getdate(today()):
            frappe.throw(_("Sorry, this coupon code's validity has expired"))
    if coupon.maximum_use:            
        if coupon.used >= coupon.maximum_use:
            frappe.throw(_("Sorry, this coupon code is no longer valid"))


@frappe.whitelist()
def get_value(field_name = None, net_total=None):
    if field_name is None:
        frappe.throw("Please enter a coupon code")

    coupon = frappe.get_doc('Coupon Code', {'coupon_code': field_name})
    if coupon is None:
        frappe.throw("Invalid Coupon Code")

    coupon_type = coupon.coupon_type
    pricing_rule = coupon.pricing_rule


    if coupon_type == "Gift Card":
        customer_name = coupon.customer
    else:
        customer_name =""
    
    
    validate_coupon_code(coupon.coupon_name)
    
    discount_type = frappe.db.get_value('Pricing Rule', {'name': pricing_rule}, ['rate_or_discount'])
    if discount_type == 'Discount Percentage':
        disc_val = frappe.db.get_value('Pricing Rule', {'name': pricing_rule}, ['discount_percentage'])
        disc_type = "Percentage"
    elif discount_type == 'Discount Amount':
        disc_val = frappe.db.get_value('Pricing Rule', {'name': pricing_rule}, ['discount_amount'])
        disc_type = "Amount"
    
    min_amt = frappe.db.get_value('Pricing Rule', {'name': pricing_rule}, ['min_amt'])
    max_amt = frappe.db.get_value('Pricing Rule', {'name': pricing_rule}, ['max_amt'])

    net_total_int = int(net_total)
    if min_amt:
        if min_amt>net_total_int:
            frappe.throw("Minimum amount not met")
    if max_amt:
        if max_amt<net_total_int:
            frappe.throw("Total exceeds max amount")

    data_k = {"discount_type": disc_type, "discount_value": disc_val, "customer": customer_name, "coupon_type": coupon_type}
    data = json.dumps(data_k)

    update_coupon_code_count(coupon.coupon_name, "used")
    
    #discount_rate = frappe.db.get_value('Pricing Rule', {'name': coupon}, ['rate'])
    return (data)