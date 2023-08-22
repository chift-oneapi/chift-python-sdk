import chift

chift.client_secret = "Spht8g8zMYWHTRaT1Qwy"
chift.client_id = "pZMQxOJJ6tl1716"
chift.account_id = "a8bfa890-e7ab-480f-9ae1-4c685f2a2a76"
chift.url_base = "http://localhost:8000"

consumers = chift.Consumer.all()

syncs = chift.Sync.all()

consumer = chift.Consumer.get("0e260397-997e-4791-a674-90ff6dab7caa")

products = consumer.invoicing.Product.all()

product = consumer.invoicing.Product.get("PRD_3789488")

contacts = consumer.invoicing.Contact.all()

data = {
    "first_name": "test",
    "addresses": [
        {
            "address_type": "main",
            "street": "street",
            "city": "city",
            "postal_code": "postal_code",
            "country": "BE",
        }
    ],
}
contact = consumer.invoicing.Contact.create(data)

invoices = consumer.invoicing.Invoice.all({"invoice_type": "customer_invoice"})

connections = consumer.Connection.all()
