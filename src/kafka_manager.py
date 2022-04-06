from confluent_kafka.admin import AdminClient, NewTopic

topics = [
    # topic_name, num_partition, replication_factor
    ('raw_frames', 1, 1),
    ('processed_frames', 1, 1),
    ('det_results', 1, 1),
    ('track_frames', 1, 1),
    ('track_results', 1, 1),
    ('count_results', 1, 1),
]

def create_topics():
    admin_client = AdminClient({'bootstrap.servers': 'kafka:9092'})

    # Call create_topics to asynchronously create topics.
    fs = admin_client.create_topics([
        NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor) \
            for (topic, num_partitions, replication_factor) in topics
    ])

    # Wait for each operation to finish.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))

from confluent_kafka.schema_registry import SchemaRegistryClient, Schema

SCHEMA_REGISTRY = 'http://schema-registry:8080'

def create_schema():
    schema_registry_client = SchemaRegistryClient({'url': SCHEMA_REGISTRY})
    for (schema_name, _, _) in topics:
        with open('schema/{}.json'.format(schema_name)) as fi:
            schema = Schema(fi.read(), 'AVRO')
        schema_registry_client.register_schema(schema_name, schema)
