from client import auth_client


def log_in_user(authorization):
    res = auth_client.post("/validate/", headers={
        "Authorization": "Bearer %s" % (authorization)
    })

    return res
