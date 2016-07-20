from django import template
from django.forms import BoundField

register = template.Library()

@register.filter
def bs3_input(bound_field):
	'''给input元素添加属性和值，使其适应bs3语义环境'''
	if not isinstance(bound_field, BoundField):
		return bound_field
	widget_attrs = bound_field.form.fields[bound_field.name].widget.attrs
	#add class "form-control"
	if widget_attrs.get("class"):
		widget_attrs["class"] += " %s" % "form-control"
	else:
		widget_attrs["class"] = "form-control"

	# if not widget_attrs.get("placeholder"):
	# 	if bound_field.help_text:
	# 		widget_attrs['placeholder'] = bound_field.help_text

	return bound_field



