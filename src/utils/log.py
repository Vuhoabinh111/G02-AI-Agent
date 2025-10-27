def log(log_message:any):
    from ..scripts.DEFAULT import LOG_FILE_PATH
    import datetime
    import os
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    with open(LOG_FILE_PATH, 'a', encoding="utf-8") as f:
        f.write(str(datetime.datetime.now()))
        f.write(str(log_message))
        f.write("\n")

def streaming_log(log_message:any):
    from ..scripts.DEFAULT import LOG_FILE_PATH
    with open(LOG_FILE_PATH, 'a', encoding="utf-8") as f:
        f.write(str(log_message))