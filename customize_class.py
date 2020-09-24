from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QWidget

class ListItem_with_id(QListWidgetItem):
    def __init__(self, rec_id,rec_user,rec_title,rec_note,rec_content,rec_time):
        super().__init__(rec_title)
        self.ID=rec_id
        self.USER=rec_user
        self.TITLE=rec_title
        self.NOTE=rec_note
        self.CONTENT=rec_content
        self.TIME=rec_time


class ListItem_with_content(QListWidgetItem):
    def __init__(self,rec_content):
        super().__init__()
        self.CONTENT = rec_content



