import logging
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('app')


class NoCacheMiddleware(MiddlewareMixin):
    """
    Middleware to prevent caching of sensitive pages
    """
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class SessionSecurityMiddleware(MiddlewareMixin):
    """
    Enhanced session security middleware to prevent:
    - Session hijacking
    - Session fixation
    - Unauthorized access
    """
    
    def process_request(self, request):
        if not request.user.is_authenticated:
            return None
        
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        if 'login_ip' not in request.session:
            request.session['login_ip'] = ip_address
            request.session['user_agent'] = user_agent
            logger.info(f"Session created for user: {request.user.username} from IP: {ip_address}")
            return None
        
        stored_ip = request.session.get('login_ip')
        if stored_ip != ip_address:
            logger.warning(
                f"SECURITY ALERT: IP address change detected for user {request.user.username}. "
                f"Original IP: {stored_ip}, Current IP: {ip_address}"
            )
            logout(request)
            messages.error(
                request,
                "Your session has been terminated due to a security concern. Please login again."
            )
            return redirect('homepage')
        
        stored_user_agent = request.session.get('user_agent')
        if stored_user_agent != user_agent:
            logger.warning(
                f"SECURITY ALERT: User agent change detected for user {request.user.username}. "
                f"Original: {stored_user_agent[:50]}..., Current: {user_agent[:50]}..."
            )
            logout(request)
            messages.error(
                request,
                "Your session has been terminated due to a security concern. Please login again."
            )
            return redirect('homepage')
        
        return None
    
    @staticmethod
    def get_client_ip(request):
        """
        Get the client's real IP address
        Handles proxy and load balancer scenarios
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip