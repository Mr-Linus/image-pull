package file

import (
	"bufio"
	"github.com/Mr-Linus/fast-pull/pkg/log"
	"io"
	"os"
)

func ReadImage(filename string) []string{
	var images []string
	fd,err :=  os.Open(filename)
	if err != nil{
		log.ErrPrint(err)
		return nil
	}
	r := bufio.NewReader(fd)
	for {
		b,_,err := r.ReadLine()
		if err != nil{
			if err == io.EOF {
				break
			}
			log.ErrPrint(err)
		}
		images = append(images,string(b))
	}
	return images
}