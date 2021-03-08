# Hydroxide Container

A containerized version of [Hydroxide.](https://github.com/emersion/hydroxide)

## Usage

There are two ways to use this container.

### Directly interacting with hydroxide
This is helpful if you need to run the `auth` sub-command directly or you would like to bypass the wrapper. All arguements passed after `jsckh/hydroxide` will be passed as arguments directly to `hydroxide`.

An example running `hydroxide auth` via the container:
```
$ docker run -it -v $HOME/.config/hydroxide:/home/hydroxide/.config/hydroxide:rw jsckh/hydroxide auth
```

### Using the wrapper to handle hydroxide


The wrapper converts environment variables into the flags passed into hydroxide. Nearly all the variables are optional.

The only required environment variables are `PROTONMAIL_USER` and `PROTONMAIL_PASS`, but _only_ if you choose not to mount your `auth.json` file.

**NOTE**: If you have 2-Factor enabled, you _must_ mount your `auth.json`. 

An example using `PROTONMAIL_USER` and `PROTONMAIL_PASS`:
```
$ docker run -d -p 1025:1025 -p 1143:1143 -p 8080:8080 \
    -e PROTONMAIL_USER="username@protonmail.com" \
    -e PROTONMAIL_PASS="v3ry-str0ng-pass" \
    jsckh/hydroxide
```

An example using a mounted `auth.json`:
```
$ docker run -d -p 1025:1025 -p 1143:1143 -p 8080:8080 \
    -v $HOME/.config/hydroxide:/home/hydroxide/.config/hydroxide:rw \
    jsckh/hydroxide
```

## Environemnt Variables

These environment variables are available for you to set. 

| Environment Variables      | Description                                                                    | Default    |
| -------------------------- | ------------------------------------------------------------------------------ | ---------- |
| `PROTONMAIL_USER`          | Your protonmail username. Only set this if you don't want mount your auth.json | no default |
| `PROTONMAIL_PASS`          | Your protonmail password. Only set this if you don't want mount your auth.json | no default |
| `HYDROXIDE_NO_SMTP`        | Set this to `true` if you would like to completely disable the SMTP bridge     | `false`    |
| `HYDROXIDE_NO_IMAP`        | Set this to `true` if you would like to completely disable the IMAP bridge     | `false`    | 
| `HYDROXIDE_NO_CARDDAV`     | Set this to `true` if you would like to completely disable the CARDAV server   | `false`    |
| `HYDROXIDE_SMTP_HOST`      | Set this to the hostname you want hydroxide to listen to for the SMTP bridge   | `0.0.0.0`  |
| `HYDROXIDE_IMAP_HOST`      | Set this to the hostname you want hydroxide to listen to for the IMAP bridge   | `0.0.0.0`  |
| `HYDROXIDE_CARDDAV_HOST`   | Set this to the hostname you want hydroxide to listen to for the CARDAV bridge | `0.0.0.0`  |
| `HYDROXIDE_SMTP_PORT`      | Set this to the port you want hydroxide to listen to for the SMTP bridge       | `1025`     |
| `HYDROXIDE_IMAP_PORT`      | Set this to the port you want hydroxide to listen to for the SMTP bridge       | `1143`     |
| `HYDROXIDE_CARDDAV_PORT`   | Set this to the port you want hydroxide to listen to for the SMTP bridge       | `8080`     |
| `HYDROXIDE_TLS_CERT`       | The path to the tls cert. `/path/to/cert.pem`. Should be mounted in.           | no default |
| `HYDROXIDE_TLS_KEY`        | The path to the tls key. `/path/to/key.pem`. Should be mounted in.             | no default |
| `HYDROXIDE_TLS_CLIENT_CA`  | The path to the tls client ca. `/path/to/ca.pem`. Should be mounted in.        | no default |
| `HYDROXIDE_DEBUG`          | Enables hydroxide's debug flag when set to `true`                              | `false`    |
