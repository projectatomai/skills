---
name: bitwarden-secrets
description: Fetch an API key, token or password from Bitwarden Secrets Manager with the bws CLI without ever showing it. Use when an authorized task needs a saved credential, or when working out why bws cannot reach one.
metadata:
  version: "1.0.0"
---

# Bitwarden Secrets Manager for agents

Use Bitwarden Secrets Manager (`bws`) to hand a credential to the one process that needs it. The person's password vault (`bw`) is a different product with far wider reach: do not use it, even as a fallback, unless the person tells you to.

## Rules that always apply

- Never print a credential, put it in a chat message or a prompt, write it to a log, or commit it.
- Keep a fetched value in the memory of the process that uses it. If a temporary file cannot be avoided, create it with mode 0600 and delete it when you finish.
- Fetch a credential only for a task the person authorized. Do not fetch one to back it up, to look at it or to copy it somewhere else.
- Reuse a credential that is already in the environment. Do not swap in another project's key, and do not create a new key, unless the person said to.

## Setup the person does once

1. Install the CLI (`bws`), from Bitwarden's Secrets Manager documentation.
2. In Secrets Manager, create a machine account, grant it only the projects an agent should reach, and create an access token for it.
3. Put that token in the environment variable `BWS_ACCESS_TOKEN`, in a place their shell or their operating system's keychain provides it from. They set it themselves. Do not ask them to paste it into the chat.

Check that the token is present without printing it:

```bash
[ -n "$BWS_ACCESS_TOKEN" ] && echo "token is set" || echo "BWS_ACCESS_TOKEN is not set"
```

## Find and use a secret

The machine account sees only the projects it was granted.

1. List secret names and ids only. The raw output of `bws secret list` holds the values, so never show it:

```bash
bws secret list --output json | python3 -c "import json,sys; [print(s['id'], s['key']) for s in json.load(sys.stdin)]"
```

2. Fetch only the secret you need, straight into the environment of the command that uses it:

```bash
SERVICE_API_KEY="$(bws secret get <secret-id> --output json | python3 -c "import json,sys; print(json.load(sys.stdin)['value'])")" \
  the-command-that-needs-it
```

The value lives only in that command's environment. Nothing is echoed and nothing is saved.

`bws run -- <command>` is another route: it runs a command with a project's secrets as environment variables. Use it when the person has set their projects up for it.

## When access is missing

Say exactly what is wrong: the token is not set, authentication failed, the project is not granted to this machine account, or the secret does not exist. Then tell the person the step that fixes it, such as granting the project to the machine account in the Secrets Manager web app.

Do not switch to the password vault, and do not ask the person to paste a key that is already stored in Secrets Manager. Do not change machine account grants, sign-in settings or stored secrets without their permission.
