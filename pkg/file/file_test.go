package file

import (
	"fmt"
	"testing"
)

func TestReadImage(t *testing.T) {
	images := ReadImage("./examples/image.txt")
	if images == nil {
		return
	}
	fmt.Println(images[0])
}