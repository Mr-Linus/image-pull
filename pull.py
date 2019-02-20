from __future__ import print_function
import docker
import logging
import settings
import optparse
import grpc
import grpc_lib.image_pull_pb2 as image_pull_pb2
import grpc_lib.image_pull_pb2_grpc as image_pull_pb2_grpc


def run(host, image):
    with grpc.insecure_channel(host+':50051') as channel:
        stub = image_pull_pb2_grpc.ImagePullStub(channel)
        response = stub.CheckImageExists(image_pull_pb2.ImageName(Image=image))
        if response.stats == 0:
            client = docker.client.from_env()
            client.images.pull(response.ImageMirrorName)
        else:
            response = stub.PullImage(image_pull_pb2.ImageName(Image=image))
            if response.stats == 0:
                client = docker.client.from_env()
                client.images.pull(response.ImageMirrorName)
            else:
                print("This image does not exist.")


def main():
    parser = optparse.OptionParser(
        'usage: pull.py -i <imagename> [-h <mirror server>]'
    )
    parser.add_option('-i', dest='image', type="string", help='specify images')
    parser.add_option('-s', dest='host', type="string", help='specify host')
    (options, args) = parser.parse_args()
    if options.host is None:
        if options.image is None:
            print(parser.usage)
        else:

            run(settings.host, options.image)
    else:
        run(options.host, options.image)


if __name__ == '__main__':
    main()
