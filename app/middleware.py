# app/middleware.py
import time
import logging
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# Logger ayarla
logger = logging.getLogger(__name__)

class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Request süresini ölçen middleware"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Request'i işle
        response = await call_next(request)
        
        # Süreyi hesapla
        process_time = time.time() - start_time
        
        # Response header'ına süreyi ekle
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log'a yaz
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
        
        return response

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Detaylı request loglama middleware"""
    
    async def dispatch(self, request: Request, call_next):
        # Client IP adresini al
        client_ip = request.client.host if request.client else "unknown"
        
        # Request bilgilerini logla
        logger.info(f"Request started: {request.method} {request.url.path} from {client_ip}")
        
        # Response'u al
        response = await call_next(request)
        
        # Response bilgilerini logla
        logger.info(f"Request completed: {response.status_code} - {request.method} {request.url.path}")
        
        return response

def setup_middleware(app):
    """Tüm middleware'leri uygulamaya ekle"""
    
    # CORS Middleware - Cross-Origin Resource Sharing
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Production'da belirli domain'leri belirtin
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted Host Middleware - Güvenlik için
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Production'da belirli host'ları belirtin
    )
    
    # Request Logging Middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # Request Timing Middleware
    app.add_middleware(RequestTimingMiddleware)
