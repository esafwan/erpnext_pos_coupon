from __future__ import unicode_literals
import frappe
from frappe.utils import cint, cstr, getdate, today
from frappe import throw, _
from frappe.utils.nestedset import NestedSet, get_ancestors_of, get_descendants_of
import json 


def validate_coupon_code(coupon_name):
    coupon = frappe.get_doc("Coupon Code", coupon_name)
    if coupon.valid_from:
        if coupon.valid_from > getdate(today()):
            frappe.throw(_("Sorry, this coupon code's validity has not started"))
    if coupon.valid_upto:
        if coupon.valid_upto < getdate(today()):
            frappe.throw(_("Sorry, this coupon code's validity has expired"))
    if coupon.used >= coupon.maximum_use:
        frappe.throw(_("Sorry, this coupon code is no longer valid"))


@frappe.whitelist()
def get_value(field_name):
    coupon_type = frappe.db.get_value('Coupon Code', {'coupon_code': field_name}, ['coupon_type'])
    pricing_rule = frappe.db.get_value('Coupon Code', {'coupon_code': field_name}, ['pricing_rule'])
    coupon_name = frappe.db.get_value('Coupon Code', {'coupon_code': field_name}, ['coupon_name'])

    validate_coupon_code(coupon_name)

    if coupon_type == "Gift Card":
        customer_name = frappe.db.get_value('Coupon Code', {'coupon_code': field_name}, ['customer'])
    else:
        customer_name =""
    
    if not pricing_rule:
        return ("null")
    else:
        discount_type = frappe.db.get_value('Pricing Rule', {'name': pricing_rule}, ['rate_or_discount'])
        if discount_type == 'Discount Percentage':
            disc_val = frappe.db.get_value('Pricing Rule', {'name': pricing_rule}, ['discount_percentage'])
            disc_type = "Percentage"
        elif discount_type == 'Discount Amount':
            disc_val = frappe.db.get_value('Pricing Rule', {'name': pricing_rule}, ['discount_amount'])
            disc_type = "Amount"
        else:
            return("null")

        data_k = {"discount_type": disc_type, "discount_value": disc_val, "customer": customer_name, "coupon_type": coupon_type}
        data = json.dumps(data_k)

        #discount_rate = frappe.db.get_value('Pricing Rule', {'name': pricing_rule}, ['rate'])
        return (data)