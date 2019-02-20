from __future__ import print_function
import docker
import logging
import settings
import optparse
import grpc
import grpc_lib.image_pull_pb2 as image_pull_pb2
import grpc_lib.image_pull_pb2_grpc as image_pull_pb2_grpc


def run(host, image_name):
    with grpc.insecure_channel(host+':50051') as channel:
        stub = image_pull_pb2_grpc.ImagePullStub(channel)
        response = stub.CheckImageExists(image_pull_pb2.ImageName(Image=image_name))
        if response.stats == 0:
            print("Mirror image is:"+response.ImageMirrorName)
            client = docker.client.from_env()
            print("Pulling images...")
            image_object = client.images.pull(response.ImageMirrorName)
            repo, tag = image_name.split(":")
            print("Changing the image's tag...")
            image_object.tag(repository=repo, tag=tag)
            client.images.remove(response.ImageMirrorName)
            print("Done.")
        else:
            response = stub.PullImage(image_pull_pb2.ImageName(Image=image_name))
            if response.stats == 0:
                print("Mirror image is:" + response.ImageMirrorName)
                client = docker.client.from_env()
                print("Pulling images...")
                image_object = client.images.pull(response.ImageMirrorName)
                print("Changing the image's tag...")
                repo, tag = image_name.split(":")
                image_object.tag(repository=repo, tag=tag)
                client.images.remove(response.ImageMirrorName)
                print("Done.")
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
