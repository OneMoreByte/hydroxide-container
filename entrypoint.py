#!/usr/bin/env python3

import os
import threading
import shlex
import subprocess as sp
import sys


AUTH_FILE = "/home/hydroxide/.config/hydroxide/auth.json"
PROTON_USER = os.getenv("PROTONMAIL_USER")
PROTON_PASS = os.getenv("PROTONMAIL_PASS")

NO_SMTP = os.getenv("HYDROXIDE_NO_SMTP") == "true"
NO_CARDDAV = os.getenv("HYDROXIDE_NO_CARDDAV") == "true"
NO_IMAP = os.getenv("HYDROXIDE_NO_IMAP") == "true"


def main(args):
    # If we get args, just passthrough to hydroxide
    if len(args) > 1:
        process = sp.Popen(
            ["/app/hydroxide"] + args[1:], 
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        process.wait()
    else:
        if PROTON_USER and PROTON_PASS:
            print("INFO: trying to log in to protonmail")
            do_auth(PROTON_USER, PROTON_PASS)
        elif os.path.exists(AUTH_FILE):
            print("INFO: using mounted in auth.")
        else:
            print(
                "ERROR: unable to run!",
                "Please either set PROTONMAIL_USER and PROTONMAIL_PASS",
                "or mount in your ~/.config/hydroxide/auth.json to",
                AUTH_FILE
            )
            exit(1)
        
        threads = []

        if not NO_SMTP:
            tmp = threading.Thread(target=hydroxide_run, args=("smtp",), daemon=True)
            tmp.start()
            threads.append(tmp)
        if not NO_CARDDAV:
            tmp = threading.Thread(target=hydroxide_run, args=("carddav",), daemon=True)
            tmp.start()
            threads.append(tmp)
        if not NO_IMAP:
            tmp = threading.Thread(target=hydroxide_run, args=("imap",), daemon=True)
            tmp.start()
            threads.append(tmp)
        
        for thread in threads:
            thread.join()
    

def do_auth(user, password):
    command = ["/app/hydroxide", "auth", user]
    process = sp.Popen(command, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
    out, err = process.communicate(input=f"{password}\n".encode("utf-8"))
    for line in out.decode("utf-8").split("\n"):
        if "2FA TOTP code:" in line:
            print(
                f"ERROR: 2 factor is enabled! Please use mounted {AUTH_FILE},",
                f"see README for how to generate and mount."
            )
            exit(1)
        if "Bridge password:" in line:
            bridge_password = line.split(":")[-1].strip()
    print(f"Bridge password: '{bridge_password}'")


def hydroxide_run(sub_cmd):
    name = sub_cmd.upper()
    args = get_hydroxide_args()
    command = shlex.split(f"/app/hydroxide{args} {sub_cmd}")
    process = sp.Popen(command, stdout=sp.PIPE)
    exitcode = 0
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            exitcode = process.poll()
            break
        if output:
            print(f"[{name}]: {output}")
    print(f"[{name}] ERROR: 'hydroxide {sub_cmd}' exited with {exitcode}")
    exit()


def get_hydroxide_args():
    args = ""
    if os.getenv("HYDROXIDE_DEBUG") == "true":
        args += " -debug"
    if os.getenv("HYDROXIDE_SMTP_HOST"):
        args += f" -smtp-host {os.getenv('HYDROXIDE_SMTP_HOST')}"
    if os.getenv("HYDROXIDE_IMAP_HOST"):
        args += f" -imap-host {os.getenv('HYDROXIDE_IMAP_HOST')}"
    if os.getenv("HYDROXIDE_CARDDAV_HOST"):
        args += f" -carddav-host {os.getenv('HYDROXIDE_CARDDAV_HOST')}"
    if os.getenv("HYDROXIDE_SMTP_PORT"):
        args += f" -smtp-port {os.getenv('HYDROXIDE_SMTP_PORT')}"
    if os.getenv("HYDROXIDE_IMAP_PORT"):
        args += f" -imap-port {os.getenv('HYDROXIDE_IMAP_PORT')}"
    if os.getenv("HYDROXIDE_CARDDAV_PORT"):
        args += f" -carddav-port {os.getenv('HYDROXIDE_CARDDAV_PORT')}"
    if os.getenv("HYDROXIDE_TLS_CERT"):
        args += f" -tls-cert {os.getenv('HYDROXIDE_TLS_CERT')}"
    if os.getenv("HYDROXIDE_TLS_KEY"):
        args += f" -tls-key {os.getenv('HYDROXIDE_TLS_KEY')}"
    if os.getenv("HYDROXIDE_TLS_CLIENT_CA"):
        args += f" -tls-client-ca {os.getenv('HYDROXIDE_TLS_CLIENT_CA')}"
    return args

if __name__ == "__main__":
    main(sys.argv)
