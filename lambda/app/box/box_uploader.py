from boxsdk import Client
from typing import Optional
from config import BoxConfig
from datetime import datetime


class BoxUploader:
    def __init__(self, client: Client, config: BoxConfig):
        self.client = client
        self.config = config

    def upload_file(self, local_file_path: str) -> (any, str):
        folder_id = self.config.box_dist_folder_id
        file_name = f"{datetime.now().strftime('%Y-%m-%d')}_{self.config.box_dist_file_name}"
        with open(local_file_path, "rb") as f:
            existing_file_id = self._find_existing_file(folder_id, file_name)
            if existing_file_id:
                existing_file = self.client.file(existing_file_id).get()
                file_info = existing_file.update_contents_with_stream(f)
            else:
                folder = self.client.folder(folder_id).get()
                file_info = folder.upload_stream(f, file_name)

        # TODO: access を適切な設定にする
        file_info.create_shared_link(access=None)
        shared_link = self.client.file(file_info.id).get().shared_link
        result = {
            "box_file_name": file_info.name,
            "box_file_id": file_info.id, 
            "box_folder_id": folder_id, 
            "shared_link": shared_link["url"]
        }
        print(f"Uploaded new file: {result}")
        return result

    def _find_existing_file(self, box_folder_id: str, box_file_name: str) -> Optional[str]:
        folder = self.client.folder(box_folder_id).get()
        items = folder.get_items()
        for item in items:
            if item.type == "file" and item.name == box_file_name:
                return item.id
        return None
