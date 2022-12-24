from application import init_app

app = init_app()
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)