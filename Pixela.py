import os
from datetime import datetime as datetime
import requests


class Pixela:
    today = datetime.now().strftime("%Y%m%d")
    USER_NAME = os.environ.get("PIXELA_USERNAME")
    TOKEN = os.environ.get("PIXELA_TOKEN")
    GRAPH_ID = "graph-1"
    user_endpoint = "https://pixe.la/v1/users"
    graph_endpoint = f"{user_endpoint}/{USER_NAME}/graphs"
    pixel_endpoint = f"{user_endpoint}/{USER_NAME}/graphs/{GRAPH_ID}"

    @staticmethod
    #     returns a response string
    def update_pixel(amt_time: float) -> str:
        pixel_config_put = {
            "quantity": str(amt_time)
        }
        headers = {
            "X-USER-TOKEN": Pixela.TOKEN
        }
        response = requests.put(url=f"{Pixela.pixel_endpoint}/{Pixela.today}", headers=headers, json=pixel_config_put)
        if response.json()["isSuccess"]:
            return "Okay I've added it to the graph"
        else:
            print(response.text)
            return "Something seems to have gone wrong, please try again"
    @staticmethod
    def get_user_link(user: str) -> str:
        if not user:
            user = Pixela.USER_NAME
        url = f"https://pixe.la/@{user}"
        return url

    @staticmethod
    def pin_graph(user_id:str ,graph_id: str) -> str:
        if not graph_id:
            graph_id = Pixela.GRAPH_ID
        if not user_id:
            user_id = Pixela.USER_NAME
        param = {
            "pinnedGraphID": graph_id
        }
        headers = {
            "X-USER-TOKEN": Pixela.TOKEN
        }
        try:
            response = requests.put(url=Pixela.get_user_link(user_id), json=param, headers=headers)
            response.raise_for_status()
            return "Graph pinned successfully"
        except requests.exceptions.HTTPError as err:
            print(err)
            return "Something seems to have gone wrong, please try again"
