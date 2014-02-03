def site_address(request):
    if request.is_secure():
        address_template = 'https://%s'
    else:
        address_template = 'http://%s'
    return {'SITE_ADDRESS': address_template % request.get_host()}
