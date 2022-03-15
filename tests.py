from sevDesk import sevDesk, get_phone_mail_from_communications
from secret_data import sev_mail, api_token

sd = sevDesk(sev_mail, api_token)
mydata = sd.get_contacts()

communications = sd.get_communication_ways()

customer_id = 'some id'
print(get_phone_mail_from_communications(communications, customer_id))
