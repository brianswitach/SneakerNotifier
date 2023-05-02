import time
import requests
from twilio.rest import Client

# Set up Twilio client and recipient phone number
account_sid = ''
auth_token = ''
twilio_phone_number = ''
recipient_phone_number = ''
client = Client(account_sid, auth_token)

# Send message indicating that code is running
message = client.messages.create(
    body='Running!',
    from_=twilio_phone_number,
    to=recipient_phone_number
)

# Set up product checking loop
urls = [
    'https://www.grid.com.ar/dunk?_q=dunk&map=ft',
    'https://www.moov.com.ar/buscar?q=dunk&search-button=&lang=null',
    'https://drifters.com.ar/productos/search:zapatilla%20nike%20sb',
    'https://fitzrovia.com.ar/24-hombres?q=Marca-Nike',
    'https://www.treeskate.com/nike-pviyh',
]
current_products = {url: set() for url in urls}

while True: 
    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Error: {response.status_code} for {url}')
        else:
            html = response.content.decode('utf-8')
            product_names = set([name.strip() for name in html.split('<span class="product-name">')[1:]])
            new_products = product_names - current_products[url]
            if new_products:
                print(f'New products available at {url}:')
                for product in new_products:
                    print(product)
                    # Send message to phone number
                    message = client.messages.create(
                        body=f'New product available at {url}: {product}',
                        from_=twilio_phone_number,
                        to=recipient_phone_number
                    )
                current_products[url] = product_names
            else : 
                print('working')
                print('')
                print('----------------')
                print('')
                print('checking again in 60 seconds')
    time.sleep(60) # Wait for 60 seconds before checking again
