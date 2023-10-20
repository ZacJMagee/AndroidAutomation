import random
import time


def random_sleep(min_seconds=5, max_seconds=15):
    """
    Sleeps the script for a random duration between min_seconds and max_seconds.

    Args:
    - min_seconds (int): Minimum seconds to sleep.
    - max_seconds (int): Maximum seconds to sleep.

    Returns:
    - None
    """
    sleep_time = random.uniform(min_seconds, max_seconds)
    time.sleep(sleep_time)


if __name__ == "__main__":
    # Test the random_sleep function
    print("Sleeping...")
    random_sleep()
    print("Awake!")
