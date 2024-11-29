# CS536 Final Project

- `quiche-client` is a QUIC http3 client
- `quiche-server` is a QUIC http3 server

Use the `-h` flag to pull up the help screen to see what options there are for both executables.

- quiche/certs contains the cert and key necessary to run `quiche-server`
- quiche/files contains the files served by `quiche-server` (can set the quiche/files as the root directory for `quiche-server`)

Following the a similar setup as assignment 0, create new terminals as necessary to handle commands that do not terminate on their own:

```
$ make controller
$ make mininet
$ make mininet-prereqs
$ make cli
$ app activate fwd (inside the cli)
$ make netcfg
```

> TODO: Figure out why quiche-server is breaking when running quiche-client from a different node

Run `make host-h1` and then
```
$ ./quiche-server --cert quiche/certs/cert.crt --key quiche/certs/cert.key --root quiche/files --listen 10.0.0.1:4433
```

Run `make host-h2` and then
```
$ ./quiche-client 10.0.0.1:4433 --no-verify
```
