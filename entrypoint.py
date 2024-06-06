#!/usr/bin/env python3

import os
import subprocess as sp
import sys

import pexpect


class Hydroxide:

    def __init__(self):
        self.auth_file = "/home/hydroxide/.config/hydroxide/auth.json"
        self.proton_user = os.getenv("PROTONMAIL_USER")
        self.proton_pass = os.getenv("PROTONMAIL_PASS")

    def entrypoint(self, args: list[str]) -> int:
        # If we get args, just passthrough to hydroxide
        if len(args) > 1:
            process = sp.Popen(
                ["/app/hydroxide"] + args[1:],
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
            )
            process.wait()
        else:
            if self.proton_user and self.proton_pass:
                print("INFO: trying to log in to protonmail")
                rc = self.auth()
                if rc != 0:
                    return rc
            elif os.path.exists(self.auth_file):
                print("INFO: using mounted in auth.")
            else:
                print(
                    "ERROR: unable to run!",
                    "Please either set PROTONMAIL_USER and PROTONMAIL_PASS",
                    "or mount in your ~/.config/hydroxide/auth.json to",
                    self.auth_file,
                )
                return 1
        return self.serve()

    def auth(self) -> int:
        command = f"/app/hydroxide auth {self.proton_user}"
        child = pexpect.spawn(command)
        child.expect("Password:")
        child.sendline(self.proton_pass)
        child.expect(pexpect.EOF)
        bridge_password = None
        for line in child.before.decode("utf-8").split("\n"):
            if "2FA TOTP code:" in line:
                print(
                    f"ERROR: 2 factor is enabled! Please use mounted {self.auth_file},",
                    f"see README for how to generate and mount.",
                )
                return 1
            if "Bridge password:" in line:
                bridge_password = line.split(":")[-1].strip()
        if not bridge_password:
            print("couldn't get bridge_password!")
            return 1
        print(f"Bridge password: '{bridge_password}'")
        return 0

    def serve(self) -> int:
        args = self._get_hydroxide_args()
        command = ["/app/hydroxide"] + args + ["serve"]
        print("running command: ", command)
        process = sp.Popen(command, stdout=sp.PIPE)
        exitcode = 0
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                exitcode = process.poll()
                break
            if output:
                print(f"[serve]: {output.decode('utf-8')}")
        print(f"[serve] ERROR: 'hydroxide serve' exited with {exitcode}")
        return exitcode

    @staticmethod
    def _get_hydroxide_args() -> list[str]:
        args = []
        if os.getenv("HYDROXIDE_DEBUG") == "true":
            args.append("-debug")
        if os.getenv("HYDROXIDE_SMTP_HOST"):
            args += ["-smtp-host", os.getenv('HYDROXIDE_SMTP_HOST')]
        if os.getenv("HYDROXIDE_IMAP_HOST"):
            args += ["-imap-host", os.getenv('HYDROXIDE_IMAP_HOST')]
        if os.getenv("HYDROXIDE_CARDDAV_HOST"):
            args += ["-carddav-host", os.getenv('HYDROXIDE_CARDDAV_HOST')]
        if os.getenv("HYDROXIDE_SMTP_PORT"):
            args += ["-smtp-port", f"{os.getenv('HYDROXIDE_SMTP_PORT')}"]
        if os.getenv("HYDROXIDE_IMAP_PORT"):
            args += ["-imap-port", os.getenv('HYDROXIDE_IMAP_PORT')]
        if os.getenv("HYDROXIDE_CARDDAV_PORT"):
            args += ["-carddav-port", os.getenv('HYDROXIDE_CARDDAV_PORT')]
        if os.getenv("HYDROXIDE_TLS_CERT"):
            args += ["-tls-cert", os.getenv('HYDROXIDE_TLS_CERT')]
        if os.getenv("HYDROXIDE_TLS_KEY"):
            args += ["-tls-key", os.getenv('HYDROXIDE_TLS_KEY')]
        if os.getenv("HYDROXIDE_TLS_CLIENT_CA"):
            args += ["-tls-client-ca", os.getenv('HYDROXIDE_TLS_CLIENT_CA')]
        if os.getenv("HYDROXIDE_NO_SMTP") == "true":
            args.append("-disable-smtp")
        if os.getenv("HYDROXIDE_NO_CARDDAV") == "true":
            args.append("-disable-carddav")
        if os.getenv("HYDROXIDE_NO_IMAP") == "true":
            args.append("-disable-imap")
        return args


if __name__ == "__main__":
    Hydroxide().entrypoint(sys.argv)
