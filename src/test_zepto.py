import requests

url = "https://api.zeptomail.eu/v1.1/email"

payload = ("{\n\"from\": { \"address\": \"noreply@microlecturi.ro\"},\n\"to\": [{\"email_address\": {\"address\": "
           "\"contact@microlecturi.ro\",\"name\": \"Micro\"}}],\n\"subject\":\"Test Email\",\n\"htmlbody\":\"<div><b> "
           "Test email sent successfully.  </b></div>\"\n}")
headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'authorization': "Zoho-enczapikey yA6KbHsM6QyhxjkGQ0k91sWKpd1lr6xo2yq14S3rK8YnKdi1j6E51xplJNe6JmTf0IaA6foCbNkTdtu"
                     "/uN5WLZc3YddQKJTGTuv4P2uV48xh8ciEYNYvjZqgArIVFK9JchggCis4RfkoWA==",
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
