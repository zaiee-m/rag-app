import threading
# The sessions dictionary that will be accessible across both threads.
# This is required because the session object itself does not exist beyond
# the window when a request is handled.
active_sessions = {}
# A lock to prevent from both the threads trying to access the dict
# at the same time and causing unpredictable bahaviour.
lock = threading.Lock()
