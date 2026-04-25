"""
Rate limiting utility.
Initializes the SlowAPI limiter.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter: Limiter = Limiter(key_func=get_remote_address)
