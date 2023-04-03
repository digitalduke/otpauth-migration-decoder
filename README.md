# otpauth migration decoder

Convert Google Authenticator data to plain otpauth links


## usage

1. get QR code in "Google Authenticator" app (Menu → Transfer accounts → Export accounts → Select accounts → Next)
1. extract link from QR code with your preferred [QR codes reading software](https://play.google.com/store/search?q=qr%20code%20reader)
1. pass migration link (`otpauth-migration://offline?data=...`) to this tool

## example

```
$ python decoder.py decode --migration "otpauth-migration://offline?data=CjEKCkhlbGxvId6tvu8SGEV4YW1wbGU6YWxpY2VAZ29vZ2xlLmNvbRoHRXhhbXBsZTAC"
```

## setup from scratch

You need to have some prerequisites installed on system, such as: `python`, `direnv`, `poetry`.

clone project
```.shell
$ git clone https://github.com/digitalduke/otpauth-migration-decoder.git
$ cd otpauth-migration-decoder
```

create virtual environment
```.shell
$ cp .envrc.example
$ direnv allow
```

activate environment, for example: `source .direnv/python-3.11.2/bin/activate.fish`
and install project requirements
```.shell
$ poetry install
```

run tests & checks
```.shell
$ tox
```

## references

1. [otpauth:// URI format](https://github.com/google/google-authenticator/wiki/Key-Uri-Format)
1. [Protocol Buffer Basics: Python](https://developers.google.com/protocol-buffers/docs/pythontutorial)
1. [Authenticator live demo](https://rootprojects.org/authenticator/)
