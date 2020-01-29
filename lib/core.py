import docker
import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcr.request.v20160607 import GetImageLayerRequest


def Check(ImageName):
    apiClient = AcsClient(settings.id, settings.key, settings.Region_id)
    namespace, nametag = ImageName.split('/')[-2:]
    image, tag = nametag.split(':')
    if tag is None:
        tag = "latest"
    try:
        request = GetImageLayerRequest.GetImageLayerRequest()
        request.set_RepoName(image)
        request.set_RepoNamespace(settings.RepoNamespace)
        request.set_Tag(tag)
        request.set_endpoint(settings.End_point)
        response = eval(apiClient.do_action_with_exception(request). decode('utf-8'))
        if response['data']['image'] == {}:
            print("This tag does not exist,Trying to call sync it.")
            return 1, ""
        else:
            print(
                "Mirror Image Exist: " +
                settings.RepoUrl +
                "/" +
                settings.RepoNamespace +
                "/" +
                image +
                ":" +
                tag)
            return 0, settings.RepoUrl + "/" + settings.RepoNamespace + "/" + image + ":" + tag
    except ServerException:
        print("The image repo does not exists,trying to create it.")
        """
        request = CreateRepoRequest.CreateRepoRequest()
        request.add_path_param("RepoName", image+"/")
        response = eval(client.AcsClient(settings.id, settings.key, 'cn-hangzhou').do_action_with_exception(request).
                        decode('utf-8'))
        """
        return 1, ""


def Sync(ImageName):

    try:
        namespace, nametag = ImageName.split('/')[-2:]
        imagename, tag = nametag.split(':')
    except BaseException:
        print("Image Name Error: " + ImageName)
        return 1, ""
    docker_client = docker.from_env()
    try:
        docker_client.api.login(
            username=settings.username,
            password=settings.password,
            registry=settings.RepoUrl)
        print("Pulling image: " + ImageName)
        image = docker_client.images.pull(ImageName)
        image.tag(
            repository=settings.RepoUrl +
            "/" +
            settings.RepoNamespace +
            "/" +
            imagename,
            tag=tag)
        print(
            "Pushing image: " +
            settings.RepoUrl +
            "/" +
            settings.RepoNamespace +
            "/" +
            imagename +
            ":" +
            tag)
        docker_client.images.push(
            repository=settings.RepoUrl +
            "/" +
            settings.RepoNamespace +
            "/" +
            imagename,
            tag=tag)
        docker_client.images.remove(
            settings.RepoUrl +
            "/" +
            settings.RepoNamespace +
            "/" +
            imagename +
            ":" +
            tag)
        docker_client.images.remove(ImageName)
        print("Done!")
        return 0, settings.RepoUrl + "/" + \
            settings.RepoNamespace + "/" + imagename + ":" + tag
    except BaseException:
        print("Sync Error!")
        return 1, ""


if __name__ == '__main__':
    Check(ImageName="k8s.gcr.io/kube-proxy-amd64:v1.11.0")
    # print("quay.io/coreos/flannel:lastest".split("/")[-2:])
