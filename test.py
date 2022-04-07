import requests as r


signup_url = "http://localhost:5000/signup"
login_url = "http://localhost:5000/login"
create_url = "http://localhost:5000/create_file"
get_url = "http://localhost:5000/get_file"
update_url = "http://localhost:5000/update_file"
delete_url = "http://localhost:5000/delete_file"


signup_data = {
    "name" : "test",
    "email": "test@test.com",
    "password": "test"
}

login_data = {
    "email": "test@test.com",
    "password": "test"
}



create_data = {
    "body": "test"
}




res_signup = r.post(signup_url, data=signup_data)
print(res_signup.text)


res_login = r.post(login_url, data=login_data)
print(res_login.json())


token = res_login.json()['token']
headers = {'x-access-token' : token}


res_create = r.post(create_url, data=create_data, headers=headers)
print(res_create.json())


file_name = res_create.json()['uuid']


get_data = {
    "file_name": file_name
}

update_data = {
    "file_name": file_name,
    "body": "Updated Test"
}

delete_data = {
    "file_name": file_name
}




res_get = r.post(get_url, data=get_data, headers=headers)
print(res_get.json())


res_update = r.post(update_url, data=update_data, headers=headers)
print(res_update.json())


res_delete = r.post(delete_url, data=delete_data, headers=headers)
print(res_delete.json())
