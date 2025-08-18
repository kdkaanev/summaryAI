# myproject/middleware.py
import logging
import traceback
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class CustomErrorLoggingMiddleware:
    """
    Middleware за улавяне на всички exceptions и логване
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"❌ Exception: {str(e)}\n{error_trace}")
            return JsonResponse(
                {"error": "Internal server error", "details": str(e)},
                status=500,
            )
