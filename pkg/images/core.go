package images

import (
	"errors"
	"github.com/Mr-Linus/fast-pull/pkg/log"
	"strings"
)
var sDomain = []string{
	"k8s.gcr.io",
	"quay.io",
	"gcr.io",
}

var azDomain = map[string]string{
	"k8s.gcr.io": "gcr.azk8s.cn",
	"quay.io": "quay.azk8s.cn",
	"gcr.io":"gcr.azk8s.cn",
}

var ustcDomain = map[string]string{
	"k8s.gcr.io": "gcr.mirrors.ustc.edu.cn/google-containers",
	"gcr.io":"gcr.mirrors.ustc.edu.cn",
	"quay.io": "quay.mirrors.ustc.edu.cn",
}

func checkImage(image string) bool{
	if image != ""{
		if strings.Contains(image,".") && strings.Contains(image,"/"){
			return true
		}
	}
	return false
}

func changeDomain(oldImage string, do map[string]string) (string, error){
	if !checkImage(oldImage){
		return "", errors.New("Image name is invalid! ")
	}
	domain := strings.Split(oldImage,"/")[0]
	for _, old := range sDomain{
		if strings.Contains(domain,old){
			if _,ok := do[old];ok{
				return strings.ReplaceAll(oldImage,old,do[old]),nil
			}
		}
	}
	return "", errors.New("The Image Domain is not gcr.io or quay.io ")
}

func SyncImage(image string) error{
	newImage, err := changeDomain(image,azDomain)
	if err != nil{
		return err
	}
	log.Print("Try to pull: "+image+" using azure ")
	log.Print("Mirror is "+newImage)
	err = DoPull(newImage)
	if err != nil{
		newImage, err = changeDomain(image,ustcDomain)
		log.Print("Try to pull: "+image+"using ustc ")
		if err = DoPull(newImage); err != nil{
			return err
		}
	}
	log.Print("Change Tags: "+image)
	err = DoTag(newImage,image)
	if err != nil{
		return err
	}
	err = DoRemove(newImage,false)
	return err
}