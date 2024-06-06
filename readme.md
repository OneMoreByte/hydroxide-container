# Hydroxide Container

A containerized version of [Hydroxide.](https://github.com/emersion/hydroxide)

## Usage

There are two ways to use this container.

### Directly interacting with hydroxide

This is helpful if you need to run the `auth` sub-command directly or you would like to bypass the wrapper. All arguments passed after `ghcr.io/onemorebyte/hydroxide` will be passed as arguments directly to `hydroxide`.

An example running `hydroxide auth` via the container:
```bash
$ docker run -it -v $HOME/.config/hydroxide:/home/hydroxide/.config/hydroxide:rw ghcr.io/onemorebyte/hydroxide auth "username@protonmail.me"
Password:
2FA TOTP code:
Bridge Password: blasjdkfsdfajlkjsdalfdsaf
```


### Using the wrapper to handle hydroxide

The wrapper converts environment variables into the flags passed into hydroxide and runs `hydroxide serve`. Nearly all the variables are optional.

The only required environment variables are `PROTONMAIL_USER` and `PROTONMAIL_PASS`, but _only_ if you choose not to mount your `auth.json` file.
> **NOTE**: If you have 2-Factor enabled, you _must_ mount your `auth.json`.

An example using `PROTONMAIL_USER` and `PROTONMAIL_PASS`:
```bash
$ docker run -d -p 1025:1025 -p 1143:1143 -p 8080:8080 \
    -e PROTONMAIL_USER="username@protonmail.com" \
    -e PROTONMAIL_PASS="v3ry-str0ng-pass" \
    -v $HOME/.config/hydroxide:/home/hydroxide/.config/hydroxide:rw
    ghcr.io/onemorebyte/hydroxide
INFO: trying to log in to protonmail
Bridge password: 'asdklfkjlsdvnmosdfavinasdopmvasdoifalklk'
running command:  ['/app/hydroxide', '-smtp-host', '0.0.0.0', '-imap-host', '127.0.0.1', '-carddav-host', '127.0.0.1', '-smtp-port', '1025', '-imap-port', '1143', '-carddav-port', '8080', 'serve']
2024/06/06 14:24:00 CardDAV server listening on 0.0.0.0:8080
2024/06/06 14:24:00 SMTP server listening on 0.0.0.0:1025
2024/06/06 14:24:00 IMAP server listening on 0.0.0.0:1143

```

An example using a mounted `auth.json`:
```bash
$ docker run -d -p 1025:1025 -p 1143:1143 -p 8080:8080 \
    -v $HOME/.config/hydroxide:/home/hydroxide/.config/hydroxide:rw \
    ghcr.io/onemorebyte/hydroxide
```


#### Creating an `auth.json` file manually
If you use 2-Factor, or you would prefer to not use the environment variables you can manually run `hydroxide auth` like the example below:
```bash
$ docker run -it -v $HOME/.config/hydroxide:/home/hydroxide/.config/hydroxide:rw ghcr.io/onemorebyte/hydroxide auth "username@protonmail.me"
Password:
2FA TOTP code:
Bridge Password: blasjdkfsdfajlkjsdalfdsaf
```

This example will create the auth.json file in your `$HOME/.config/hydroxide` directory. You can then pass that into the container to run it normally:

```bash
$ docker run -d -p 1025:1025 -p 1143:1143 -p 8080:8080 \
    -v $HOME/.config/hydroxide:/home/hydroxide/.config/hydroxide:rw
    ghcr.io/onemorebyte/hydroxide
INFO: using existing auth file.
running command:  ['/app/hydroxide', '-smtp-host', '0.0.0.0', '-imap-host', '127.0.0.1', '-carddav-host', '127.0.0.1', '-smtp-port', '1025', '-imap-port', '1143', '-carddav-port', '8080', 'serve']
2024/06/06 14:24:00 CardDAV server listening on 0.0.0.0:8080
2024/06/06 14:24:00 SMTP server listening on 0.0.0.0:1025
2024/06/06 14:24:00 IMAP server listening on 0.0.0.0:1143

```


## Environment Variables

These environment variables are available for you to set. 

| Environment Variables     | Description                                                                                                                            | Default     |
|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------|-------------|
| `PROTONMAIL_USER`         | Your protonmail username. This can be ommited if you mount the auth.json file created by running `hydroxide auth`                      | no default  |
| `PROTONMAIL_PASS`         | Your protonmail password. This can be ommited if you mount the auth.json file created by running `hydroxide auth`                      | no default  |
| `HYDROXIDE_NO_SMTP`       | Set this to `true` if you would like to completely disable the SMTP bridge                                                             | `false`     |
| `HYDROXIDE_NO_IMAP`       | Set this to `true` if you would like to completely disable the IMAP bridge                                                             | `false`     | 
| `HYDROXIDE_NO_CARDDAV`    | Set this to `true` if you would like to completely disable the CARDAV server                                                           | `false`     |
| `HYDROXIDE_SMTP_HOST`     | Set this to the hostname you want hydroxide to listen to for the SMTP bridge                                                           | `0.0.0.0` |
| `HYDROXIDE_IMAP_HOST`     | Set this to the hostname you want hydroxide to listen to for the IMAP bridge                                                           | `0.0.0.0` |
| `HYDROXIDE_CARDDAV_HOST`  | Set this to the hostname you want hydroxide to listen to for the CARDAV bridge                                                         | `0.0.0.0` |
| `HYDROXIDE_SMTP_PORT`     | Set this to the port you want hydroxide to listen to for the SMTP bridge                                                               | `1025`      |
| `HYDROXIDE_IMAP_PORT`     | Set this to the port you want hydroxide to listen to for the SMTP bridge                                                               | `1143`      |
| `HYDROXIDE_CARDDAV_PORT`  | Set this to the port you want hydroxide to listen to for the SMTP bridge                                                               | `8080`      |
| `HYDROXIDE_TLS_CERT`      | The path to the tls cert. `/path/to/cert.pem`. Should be mounted in.                                                                   | no default  |
| `HYDROXIDE_TLS_KEY`       | The path to the tls key. `/path/to/key.pem`. Should be mounted in.                                                                     | no default  |
| `HYDROXIDE_TLS_CLIENT_CA` | The path to the tls client ca. `/path/to/ca.pem`. Should be mounted in.                                                                | no default  |
| `HYDROXIDE_BRIDGE_PASS`   | The bridge password hydroxide should use. Will skip password prompt. This variable is only useful if you are using hydroxide directly. | no default  |
| `HYDROXIDE_DEBUG`         | Enables hydroxide's debug flag when set to `true`                                                                                      | `false`     |
