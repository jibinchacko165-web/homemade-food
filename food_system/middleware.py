from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):
    """
    Middleware to prevent browser caching of all pages.
    This ensures that when a user logs out, they cannot use the browser's 
    'Back' button to view their previously authenticated session pages,
    and prevents caching of login pages which can cause CSRF errors.
    """
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
