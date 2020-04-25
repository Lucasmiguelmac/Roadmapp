from django import template

register = template.Library()

@register.inclusion_tag('roadmaps/tree_structure.html')
def make_tree(item_membership):
    children_item_memberships = item_membership.children_item_memberships.all()
    return {"children_item_memberships": children_item_memberships}