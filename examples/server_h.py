from sachima import sachima_http_server


if __name__ == "__main__":
    sachima_http_server.app.run("0.0.0.0", port=8008)
