import docker
import settings
from aliyunsdkcore import client
from aliyunsdkcr.request.v20160607 import GetImageLayerRequest

def Check(ImageName):
    client.region_provider.add_endpoint(settings.Product_name,
                                        settings.Region_id,
                                        settings.End_point)
    namespace, nametag = ImageName.split('/')
    image, tag = nametag.split(':')
    request = GetImageLayerRequest.GetImageLayerRequest()
    request.set_RepoName(image)
    request.set_RepoNamespace(settings.RepoNamespace)
    request.set_Tag(tag)
    response = eval(client.AcsClient(settings.id, settings.key, 'cn-hangzhou').do_action_with_exception(request).
                    decode('utf-8'))
    if response['data']['image'] == {}:
        print("This tag does not exist.")
        return 1, ""
    else:
        print("Mirror Image is: "+settings.RepoUrl+"/"+settings.RepoNamespace+"/"+image+":"+tag)
        return 0, settings.RepoUrl+"/"+settings.RepoNamespace+"/"+image+":"+tag


def Sync(ImageName):
    namespace, nametag = ImageName.split('/')
    imagename, tag = nametag.split(':')
    docker_client = docker.from_env()
    try:
        docker_client.api.login(username=settings.username, password=settings.password, registry=settings.RepoUrl)
        image = docker_client.images.pull(ImageName)
        image.tag(repository=settings.RepoUrl+"/"+settings.RepoNamespace+"/"+imagename, tag=tag)
        docker_client.images.push(repository=settings.RepoUrl+"/"+settings.RepoNamespace+"/"+imagename, tag=tag)
        docker_client.images.remove(settings.RepoUrl+"/"+settings.RepoNamespace+"/"+imagename+":"+tag)
        docker_client.images.remove(ImageName)
        return 0, settings.RepoUrl+"/"+settings.RepoNamespace+"/"+imagename+":"+tag
    except:
        print("Sync Error!")
        return 1, ""


if __name__ == '__main__':
    Check(ImageName="k8s.gcr.io/kube-proxy-amd64:v1.11.0")
