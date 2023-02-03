from gateway.client import auth_client


def log_in_user(authorization):
    res = auth_client.post("/login/", headers={
        "Authorization": "Bearer %s" % (authorization)
    })

    if res.status_code == 200:
        return True

    return False
