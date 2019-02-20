from concurrent import futures
import time
import logging

import grpc
import grpc_lib.image_pull_pb2 as image_pull_pb2
import grpc_lib.image_pull_pb2_grpc as image_pull_pb2_grpc
from lib.core import Check, Sync

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class ImagePull(image_pull_pb2_grpc.ImagePullServicer):
    def CheckImageExists(self, request, context):
        stats, name = Check(request.Image)
        return image_pull_pb2.Results(stats=stats, ImageName=name)

    def PullImage(self, request, context):
        stats, name = Sync(request.Image)
        return image_pull_pb2.Results(stats=stats, ImageName=name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_pull_pb2_grpc.add_ImagePullServicer_to_server(ImagePull(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
