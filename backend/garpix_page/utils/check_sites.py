def check_sites(cleaned_data):
    """
    returns True if sites params same as parent or children objects (instance have same sites id as children and parent)
     or if site params of instance have no sense (instance, parent or children have no sites params,)

    return False if site params have not intersection with parent/children of instance (did not have SAME site id)
    :return: bool
    """
    result = True
    if cleaned_data.get('sites', None):
        instance_sites = set(cleaned_data['sites'].all().values_list('id', flat=True))
        if cleaned_data.get('parent', None) and cleaned_data['parent'] is not None \
           and hasattr(cleaned_data['parent'], 'sites') and cleaned_data['parent'].sites is not None:
            parent_sites = set(cleaned_data['parent'].sites.all().values_list('id', flat=True))
            result = bool(instance_sites.intersection(parent_sites))
    return result
