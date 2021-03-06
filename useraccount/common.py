import datetime
import os
import uuid

def file_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    d = datetime.dateiem.now()
    filepath = d.strftime("%Y/%M/%d")
    suffix = d.strftime("%Y%m%d%H%M%S")
    filename = "%s_%s.%s" % (uuid.uuid4().hex, suffix, ext)
    return os.path.join(filepath, filename)
