package log

import (
	"fmt"
)

func ErrPrint(err error) {
	fmt.Printf("[fast-pull] - \"Error: %s\"\n",  err)
}

func Print(log string) {
	fmt.Printf("[fast-pull] - \"%s\"\n",  log)
}

