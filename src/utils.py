import datetime

def log_progress(success, failed, start_time):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    elapsed = datetime.datetime.now() - start_time
    # Total attempted
    total = success + failed
    print(f"[{now}] Total: {total} | Success: {success} | Failed: {failed}")

def load_proxies():
    # Returning an empty list because you are not using proxies
    return []