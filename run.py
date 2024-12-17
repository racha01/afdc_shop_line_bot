from app import create_app

app = create_app()

app.secret_key = 'REPLACE ME - this value is here as a placeholder.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', 
            port=5000,
            ssl_context=('cert.pem', 'private.pem'),
            debug=True)