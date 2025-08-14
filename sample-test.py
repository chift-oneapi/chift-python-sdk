import chift

chift.client_secret = "8aWW6gpbiHkAWOIlBGzO"
chift.client_id = "nx2c5aJKURF53rL"
chift.account_id = "00fc1383-b743-4c9c-8cd6-a90a3dc811e0"
chift.url_base = "http://chift.localhost:8000"

consumers = chift.Consumer.all()

syncs = chift.Sync.all()

consumer = chift.Consumer.get("7ad965d8-b37c-49f1-bbf8-ad36e2f5bba6")


consumer.accounting.AnalyticAccountMultiPlan.all()



