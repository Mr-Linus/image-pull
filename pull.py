from __future__ import print_function
import docker
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
            try:
                image_object.tag(repository=repo, tag=tag)
            except:
                print("Change Tag error!The Image Name maybe exist.")
            client.images.remove(response.ImageMirrorName)
            print("Done.")
        else:
            print("The image does not exist in the repository, \n" +
                  "try to pull from the original Repo: \n" +
                  image_name)
            response = stub.PullImage(image_pull_pb2.ImageName(Image=image_name))
            if response.stats == 0:
                print("Sync Finished,Mirror image is:" + response.ImageMirrorName)
                client = docker.client.from_env()
                print("Pulling images...")
                image_object = client.images.pull(response.ImageMirrorName)
                print("Changing the image's tag...")
                repo, tag = image_name.split(":")
                try:
                    image_object.tag(repository=repo, tag=tag)
                except:
                    print("Change Tag error!The Image Name maybe exist.")
                client.images.remove(response.ImageMirrorName)
                print("Done.")
            else:
                print("This image does not exist.")


def main():
    parser = optparse.OptionParser(
        'usage: pull.py -i <imagename> e.g: quay.io/coreos/flannel:v0.11.0 [-f <imagename-file>] | [-h <mirror server>]'
    )
    parser.add_option('-i', dest='image', type="string", help='specify images')
    parser.add_option('-s', dest='host', type="string", help='specify host')
    parser.add_option('-f', dest='filename', metavar="FILE", help='specify image-name file')
    (options, args) = parser.parse_args()
    if options.host is None:
        host = settings.host
    else:
        host = options.host
    if (options.image is None) and (options.filename is not None):
        try:
            with open(options.filename) as f:
                line = f.readline().replace('\n', '')
                while line:
                    print("Get image:"+line)
                    run(host, str(line))
                    line = f.readline().replace('\n', '')
        except:
            print("Read the file:"+options.filename+" Error! or Docker is not running!")
    elif options.image is not None:
        run(host, options.image)
    else:
        print(parser.usage)


if __name__ == '__main__':
    main()
