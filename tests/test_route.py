
                    
def test_home_page(client):
    res = client.get("/")        
    assert res.status_code == 200
    assert b"<title>Home Page</title>" in res.data


def test_event_page(client):
    res = client.get("/event")
    assert res.status_code == 401


def test_logout_redirect(client):
    res =  client.get("/logout", follow_redirects = True)
    assert len(res.history) == 1
    assert res.request.path == "/login"
