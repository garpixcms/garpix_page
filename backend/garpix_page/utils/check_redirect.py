def check_redirect(request, context):
    """
    if 'redirect' key in context dict than redirects to url ('redirect':value).
    request is need to exclude recursive redirect
    :param request:
    :param context:
    :return: httpresponse : redirects to given url
    """
    redirect_context = context.get('redirect', None)
    if redirect_context and request.path != redirect_context:
        return context['redirect']
