package images

import (
	"bytes"
	"github.com/Mr-Linus/fast-pull/pkg/log"
	"github.com/docker/docker/api/types"
	"github.com/docker/docker/client"
	"golang.org/x/net/context"
)

func DoPull(image string) error {
	ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.WithVersion("1.37"))
	if err != nil {
		return err
	}
	out, err := cli.ImagePull(ctx, image, types.ImagePullOptions{All: false})
	if err != nil {
		log.ErrPrint(err)
	}
	defer func() {
		_ = out.Close()
	}()
	if _, err := new(bytes.Buffer).ReadFrom(out); err != nil {
		log.ErrPrint(err)
	}
	return err
}

func DoRemove(imageName string, force bool) error {
	ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.WithVersion("1.37"))
	if err != nil {
		log.ErrPrint(err)
	}
	if _, err := cli.ImageRemove(ctx, imageName, types.ImageRemoveOptions{Force: force}); err != nil {
		log.ErrPrint(err)
	}
	return err
}

func DoTag(oldImage, newImage string) error {
	ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.WithVersion("1.37"))
	if err != nil {
		log.ErrPrint(err)
	}
	if err := cli.ImageTag(ctx,oldImage,newImage); err != nil{
		log.ErrPrint(err)
	}
	return err
}