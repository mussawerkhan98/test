from app import app, add
 
 
def test_add():
    assert add(2, 3) == 5
 
 
def test_health_route_exists():
    # Checks the /health URL is registered (doesn't need MongoDB)
    routes = [r.rule for r in app.url_map.iter_rules()]
    assert "/health" in routes