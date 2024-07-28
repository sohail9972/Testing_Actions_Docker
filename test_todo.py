import requests
import uuid


ENDPOINT= "https://todo.pixegami.io/"

response= requests.get(ENDPOINT)
print(response)

data = response.json()
print(data)

status_code =response.status_code
print(status_code)


def test_can_call_endPoint():
    response = requests.get(ENDPOINT)
    assert response.status_code ==200
    pass

def test_can_create_task():
    payload=new_task_payload()
    # response=requests.put(ENDPOINT + "/create-task",json=payload)
    response = create_task(payload)
    assert response.status_code==200
    data= response.json()
    # print(data)
    # getting the task ID to confirmation of the Update
    task_id= data["task"]["task_id"]
    # get_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    get_response = get_task(task_id)

    assert get_response.status_code==200
    get_response_data = get_response.json()
    assert get_response_data["content"]==payload["content"]
    assert get_response_data["user_id"]==payload["user_id"]

    # print(get_response)

    # updating the data

def test_can_update_task():
    payload=new_task_payload()
    response = create_task(payload)
    assert response.status_code==200
    task_id = response.json()["task"]["task_id"]

    # update the task
    new_paylaod = {
        "user_id":payload["user_id"],
        "task_id":task_id,
        "content" : "my updated content",
        "is_done":True,
    }
    update_task_response = update_task(new_paylaod)
    # print(update_task_response)
    assert update_task_response.status_code==200

    # hitting the Get Api call to validate the response thats been updated

    get_response = get_task(task_id)
    assert get_response.status_code==200
    get_task_data = get_response.json()
    assert get_task_data["content"] == new_paylaod["content"]
    assert get_task_data["is_done"]==new_paylaod["is_done"]



def test_can_list_users():
    # creatingN tasks
    n=3
    payload = new_task_payload()
    for _ in range(n):

        response = create_task(payload)
        assert response.status_code==200

    user_id = payload["user_id"]
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code==200
    data = list_task_response.json()

    tasks= data["tasks"]
    assert len(tasks)==n
    print(data)
    pass



def test_can_delete_task():
    # crete,Delete, Check the task by Get call
    payload = new_task_payload()
    response = create_task(payload)
    assert response.status_code==200
    task_id = response.json()

    # deleting the Task
    delere_task_response= delete_taask(task_id)
    assert delere_task_response.status_code==200

    # get call to confirm the task is deleted
    get_task_response= get_task(task_id)
    assert get_task_response.status_code==404
    # print(get_task_response.status_code)
    pass





def create_task(payload):
    return requests.put(ENDPOINT + "/create-task",json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task",json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def delete_taask(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")
def new_task_payload():
    user_id=f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    print(f"Creating task for user {user_id} with content {content}")
    return {
        "content": "my test content",
        "user_id": user_id,
        "is_done": False,
    }