from main import app
from fastapi.routing import APIRoute
for route in app.router.routes:
    if isinstance(route, APIRoute):
        print(f"  {','.join(sorted(route.methods)):10s}  {route.path}")
