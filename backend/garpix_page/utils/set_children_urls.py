
def set_children_url(instance, children, pages_to_update):
    pages_to_update += list(children)
    for page in children:
        page.set_url(parent=instance)
        children = page.get_children()
        if any(children):
            set_children_url(page, children, pages_to_update)
