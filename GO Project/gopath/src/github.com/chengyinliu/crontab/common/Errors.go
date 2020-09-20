package common

import "errors"

var (
	ERR_LOCK_ALREADY_REQUIRED = errors.New("lock is occupied")
	ERR_NO_LOCAL_IP_FOUND = errors.New("no local ip")
)