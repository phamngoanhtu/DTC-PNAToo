import json
import numpy as np
from similaritymeasures import frechet_dist

from kafka_messenger import KafkaProducer, KafkaConsumer

MOI_json = json.load(open('MOI_DuongBaTrac-TaQuangBuu-1.json'))
MOIs = [(MOI['shape_attributes']['all_points_x'],MOI['shape_attributes']['all_points_y'])
            for MOI in MOI_json]
MOIs = [list(zip(MOI[0],MOI[1])) for MOI in MOIs]

if __name__ == '__main__':
    consumer = KafkaConsumer('track_results')
    producer = KafkaProducer('count_results')
    while True:
        msg = consumer.consume()

        if msg is None:
            continue

        video_id = msg.key()
        value = msg.value()
        track_id = value['track_id']
        bbox = value['bbox']

        track = [((bb[0] + bb[2]) // 2, (bb[1] + bb[3]) // 2) for bb in bbox]
        moi_id = np.argmin([frechet_dist(track, MOI) for MOI in MOIs])

        value = {
            'track_id': track_id,
            'moi_id': moi_id
        }

        producer.produce(
            key=video_id, 
            value=value
        )