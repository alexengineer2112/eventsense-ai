import schedule
import time
from eventsense_ai import main


def run_job():
    print("\n🚀 Running placement email monitor...\n")
    main()


# Run once at start
run_job()

# Run every 6 hours
schedule.every(12).hours.do(run_job)


print("🤖 AI Email Monitor Started...")
print("Checking placement emails every 6 hours...\n")

while True:
    schedule.run_pending()
    time.sleep(60)