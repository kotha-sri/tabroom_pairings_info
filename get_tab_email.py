# FOR TESTING - HTTP LOCALHOST SERVER
# start: 'python -m http.server -b 127.0.0.42 8080'
# end: ctrl + c

import os
import google

topic_name = 'projects/tab-pairings-info/topics/tab_pairings_email'.format(
    project_id=os.getenv('Tab Pairings Info'),
    topic='tab_pairings_email',  # Set this to something appropriate.
)

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=os.getenv('Tab Pairings Info'),
    sub='all_tab_emails',  # Set this to something appropriate.
)

def callback(message):
    print(message.data)
    message.ack()

with google.cloud.pubsub_v1.SubscriberClient() as subscriber:
    subscriber.create_subscription(
        name=subscription_name, topic=topic_name)
    future = subscriber.subscribe(subscription_name, callback)