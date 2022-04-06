import numpy as np
from sort import Sort
from kafka_messenger import KafkaProducer, KafkaConsumer


class TrackKafka:
    def __init__(self):
        self.consumer = KafkaConsumer('det_results')
        self.producer_tracks = KafkaProducer('track_results')
        self.producer_frames = KafkaProducer('track_frames')

    def produce_tracking_result(self):
        """ This will generate pairs of key and value from  video_id and info of trackers """
        trackers = {}
        active_tracks = {}

        while True:
            msg = self.consumer.consume()
            # consume() will return records from the last consumed offset.
            if msg is None:
                continue
            # Check if message exits

            video_id = msg.key()
            value = msg.value()
            frame_id = value['frame_id']

            tracker, active_tracks = self.create_tracker(video_id, trackers, active_tracks)
            # Create instance of SORT tracker and its container list

            bbox = np.array(value['bbox'])  # bbox = [x1, y1, x2, y2, score]
            score = np.array(value['score']).reshape(-1, 1)
            # Get bbox and score from message_pack

            tracks = self.__update_tracks(trackers, video_id, bbox, score)
            track_list = self.__update_track_list(video_id, tracker, active_tracks, tracks)

            self.__produce_result_frame(tracks, frame_id, video_id, self.producer_frames)
            # Produce result for each frame

            self.__produce_result_tracks(track_list, tracks, self.producer_tracks, video_id)
            # Produce result for each tracks

    @staticmethod
    def create_tracker(video_id, trackers, active_tracks):
        if video_id not in trackers:
            # Create instance of the SORT tracker
            trackers[video_id] = Sort(max_age=1,
                                      min_hits=1,
                                      iou_threshold=0.15)
            # Create tracks container
            active_tracks[video_id] = {}
            return [trackers, active_tracks]

    @staticmethod
    def __update_tracks(trackers, video_id, bbox, score):
        tracks = trackers[video_id].update(np.hstack((bbox, score))).astype(int).tolist()
        return tracks

    @staticmethod
    def __update_track_list(video_id, frame_id, tracks, active_tracks):
        # np.hstack() returns 1D array from both argument.
        track_list = active_tracks[video_id]
        for track in tracks:
            # track = [x1, y1, x2, y2, id]
            if track[-1] not in track_list:
                track_list[track[-1]] = {
                    'id': int(track[-1]),
                    'history': [],
                }
            track_list[track[-1]]['history'].append((track[:4], frame_id))
        return track_list

    @staticmethod
    def __produce_result_frame(tracks, frame_id, video_id, producer_frames):
        track_frames = [track[:4] for track in tracks]
        track_id = [track[4] for track in tracks]
        value = {'frame_id': frame_id,
                 'bbox': track_frames,
                 'track_id': track_id,
                 'class': [0 for _ in track_id]}
        producer_frames.produce(key=video_id,
                                value=value)

    @staticmethod
    def __produce_result_tracks(track_list, tracks, producer_tracks, video_id):
        tracks = {track[-1] for track in tracks}
        for track_id in (set(track_list) - tracks):
            track = track_list.pop(track_id)['history']
            bbox = [bb[0] for bb in track]
            frame_id = [bb[1] for bb in track]
            value = {
                'track_id': int(track_id),
                'bbox': bbox,
                'frame_id': frame_id,
                'class': [0 for _ in frame_id]
            }
            producer_tracks.produce(
                key=video_id,
                value=value
            )

