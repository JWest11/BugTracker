import os
import shutil
from flask import send_from_directory, Blueprint, current_app
from flaskr.auth import login_required

bp = Blueprint('files', __name__, url_prefix='/files')


def deleteTicketFiles(ticket_id):
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(ticket_id))
    if os.path.exists(path):
        shutil.rmtree(path)

@bp.route('/download/<int:ticket_id>/<string:filename>')
@login_required
def downloadFile(ticket_id, filename):
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(ticket_id))
    return send_from_directory(path, filename)