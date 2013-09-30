import os
from wtforms import Form, TextField, validators


class BoxDocument(Form):
    file_path = TextField('FilePath', [validators.Length(min=3, max=255)])

    @property
    def file_name(self):
        return os.path.basename(self.file_path.data)

    @property
    def file(self):
        path = self.file_path.data
        if os.path.exists(path):
            return open(path, 'rb')
        else:
            return None
