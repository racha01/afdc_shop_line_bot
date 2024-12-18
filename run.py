from app import create_app

app = create_app()

app.secret_key = 'REPLACE ME - this value is here as a placeholder.'
context = (
    '/etc/letsencrypt/live/afdc.shop.coding.infy.uk/fullchain.pem',
    '/etc/letsencrypt/live/afdc.shop.coding.infy.uk/privkey.pem'
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', 
            port=443,
            ssl_context=context,
            debug=True)