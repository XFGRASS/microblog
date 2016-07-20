# from django import template
# # from django.template.defaultfilters import stringfilter
# from django.forms import BoundField

# register = template.Library()

# @register.filter
# def add_elem_attrs(bound_field, attr_name_values):
# 	'''attr_name_values参数值中，元素属性和值在同一字符串中被 '=' 分割 , 每组键值对被,分割'''
# 	if not isinstance(bound_field, BoundField) or "=" not in attr_name_values:
# 		return bound_field

# 	name_values = attr_name_values.split(",")
# 	# 如果最后一组名值对有;,那么数组中最后一个元素则为""空字符
# 	if name_values[len(name_values)-1] == "":
# 		name_values.remove(len(name_values)-1) 

# 	widget_attrs = bound_field.form.fields[bound_field.name].widget.attrs
# 	for name_value in name_values:
# 		attr_name, attr_value = name_value.split('=')
# 		# 如果class已经有值，那么则空格后添加
# 		if attr_name == "class" and widget_attrs.get(attr_name):
# 			widget_attrs[attr_name] += " %s" % attr_value
# 		else:
# 			widget_attrs[attr_name] = attr_value

# 	return 


