import requests as r
from moto import mock_s3
from uuid import uuid4


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




@mock_s3
def test_signup():
    res_signup = r.post(signup_url, data=signup_data)
    assert res_signup.status_code == 200
    assert res_signup.json()["status"] == "success"



@mock_s3
def test_login():
    r.post(signup_url, data=signup_data)
    assert r.post(login_url, data=login_data).status_code == 200
    assert r.post(login_url, data=login_data).json()["token"] != None


@mock_s3
def test_create_file():
    r.post(signup_url, data=signup_data)
    res_login = r.post(login_url, data=login_data)
    token = res_login.json()['token']
    headers = {'x-access-token': token}

    res_create_file = r.post(create_url, data=create_data, headers=headers)
    assert res_create_file.status_code == 200

    
    import boto3

    s3 = boto3.resource("s3", endpoint_url="http://0.0.0.0:4566", aws_access_key_id="temp", aws_secret_access_key="temp")

    try: 
        s3.Object("localbucket", res_create_file.json()['uuid'] + ".json").load()
    except:
        assert False


@mock_s3
def test_get_file():
    r.post(signup_url, data=signup_data)
    res_login = r.post(login_url, data=login_data)
    token = res_login.json()['token']
    headers = {'x-access-token': token}

    res_create_file = r.post(create_url, data=create_data, headers=headers)
    assert res_create_file.status_code == 200

    get_data = {
        "file_name": res_create_file.json()['uuid'] + ".json"
    }

    res_get_file = r.post(get_url, data=get_data, headers=headers)
    assert res_get_file.status_code == 200
    assert res_get_file.json()['body'] == create_data['body']


@mock_s3
def test_update_file():
    r.post(signup_url, data=signup_data)
    res_login = r.post(login_url, data=login_data)
    token = res_login.json()['token']
    headers = {'x-access-token': token}

    res_create_file = r.post(create_url, data=create_data, headers=headers)
    assert res_create_file.status_code == 200

    get_data = {
        "file_name": res_create_file.json()['uuid'] + ".json"
    }

    res_get_file = r.post(get_url, data=get_data, headers=headers)
    assert res_get_file.status_code == 200
    assert res_get_file.json()['body'] == create_data['body']

    update_data = {
        "file_name": res_create_file.json()['uuid'] + ".json",
        "body": "Updated Test"
    }

    res_update_file = r.post(update_url, data=update_data, headers=headers)
    assert res_update_file.status_code == 200
    assert res_update_file.json()['body'] == update_data['body']


@mock_s3
def test_delete_file():
    r.post(signup_url, data=signup_data)
    res_login = r.post(login_url, data=login_data)
    token = res_login.json()['token']
    headers = {'x-access-token': token}

    res_create_file = r.post(create_url, data=create_data, headers=headers)
    assert res_create_file.status_code == 200

    get_data = {
        "file_name": res_create_file.json()['uuid'] + ".json"
    }

    res_get_file = r.post(get_url, data=get_data, headers=headers)
    assert res_get_file.status_code == 200
    assert res_get_file.json()['body'] == create_data['body']

    delete_data = {
        "file_name": res_create_file.json()['uuid'] + ".json"
    }

    res_delete_file = r.post(delete_url, data=delete_data, headers=headers)
    assert res_delete_file.status_code == 200

    import boto3

    s3 = boto3.resource("s3", endpoint_url="http://0.0.0.0:4566", aws_access_key_id="temp", aws_secret_access_key="temp")

    try: 
        s3.Object("localbucket", res_create_file.json()['uuid'] + ".json").load()
        assert False
    except:
        assert True

    
test_signup()
test_login()
test_create_file()
test_get_file()
test_update_file()
test_delete_file()
