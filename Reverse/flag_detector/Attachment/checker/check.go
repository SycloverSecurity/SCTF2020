package checker

// #include "check.h"
import "C"

var ret int

func Check() int {
	return int(C.machine())
}
