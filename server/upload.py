import os
from typing import Set

from werkzeug.utils import secure_filename

# todo: need to put this as global setting
UPLOAD_FOLDER = os.getcwd() + "/data/uploaded"
ALLOWED_EXTENSIONS: Set[str] = {'csv'}


def allowed_files(files):
    for file in files:
        filename = file.filename
        if ('.' not in filename and
                filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS):
            return False
    return True


# todo: checks on data that competition, matches etc. are all present
def save_to_server(game_data):
    if len(game_data) == 5 and allowed_files(game_data):
        for csv in game_data:
            filename = secure_filename(csv.filename)
            csv.save(os.path.join(UPLOAD_FOLDER, filename))
