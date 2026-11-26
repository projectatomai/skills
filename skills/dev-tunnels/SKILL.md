---
name: dev-tunnels
description: Start, restart or check local dev servers and the reserved ngrok tunnels in front of them, with one fixed port and one fixed public address per project. Use for "restart the server", "start the dev server", "ngrok", "tunnel", a request for a local or public URL, or when adding a tunnel for a new project.
metadata:
  version: "1.0.0"
---

# Dev servers and ngrok tunnels

Several projects run on one machine, each with a dev server on its own port and its own reserved ngrok address. This skill keeps the two matched, so a login callback or a webhook that points at a project's public address always reaches the right server.

## The one-agent rule

Many ngrok plans allow only one running agent at a time (check your plan). So every tunnel lives in one config file, and they start through that agent:

- `ngrok start --all` starts every tunnel in the config.
- `ngrok start <name>` starts one of them.
- Do not run `ngrok http <port> --url=<domain>` beside a running agent. It fails, because the session is already taken.

`ngrok config check` prints where the config file is. Run `ngrok start --help` if a flag is refused, because flags change between versions.

## The assignments table

Keep one table of assignments in the project's or the person's agent instructions file, and treat it as the truth:

| Project | Local port | Public address |
|---|---|---|
| example-app | 3001 | https://example-app.ngrok.app |
| example-site | 3002 | https://example-site.ngrok.app |

Reserved addresses are usually registered with outside services: OAuth providers, webhooks, payment and social APIs. Do not change which port an address points to without updating those services too, and say so before you do.

## Rules

- A dev server's port must match the table. With npm, pass the port through to the dev server, for example `npm run dev -- --port <port>` (the flag depends on the framework, and Next.js uses `-p`).
- "Restart the server" means both halves: the dev server on its port and that project's tunnel. If other projects' tunnels are running, restart only the one affected. Use `ngrok start --all` only when the whole agent was stopped.
- After starting, give the person both addresses: `http://localhost:<port>` and the public one.
- Stop only processes you can identify as this project's. Do not kill another project's server to free a port. Ask.

## Run in the background

```bash
cd <repo> && nohup npm run dev -- -p <port> > "${TMPDIR:-/tmp}/<project>-dev.log" 2>&1 &
nohup ngrok start --all > "${TMPDIR:-/tmp}/ngrok.log" 2>&1 &
```

## Check what is running

- Running agents: `pgrep -fl ngrok`
- ngrok's local page: `http://localhost:4040`. A second agent would take 4041, so check `pgrep` before you trust the port.
- The tunnels as data: `curl -s http://localhost:4040/api/tunnels`
- What holds a port: `lsof -nP -iTCP:<port> -sTCP:LISTEN`

## Add a project

1. Pick a free port and reserve an address in the ngrok dashboard. The person does this, because it is their account.
2. Add the tunnel to the ngrok config file.
3. Restart the agent so it reads the new config.
4. Add a row to the assignments table.

## Things that go wrong

- **A build while the dev server runs.** Many frameworks share one cache folder between `dev` and `build`. In Next.js, running `npm run build` beside `next dev` breaks the dev server: it returns 500s and missing chunk files. Stop the dev server, delete `.next`, and start it again.
- **The public address shows another project.** The tunnel points at the wrong port, or the wrong server took the port. Compare the table with `lsof` and the tunnels data.
- **"Session already in use".** Another agent is running. Find it with `pgrep` and start your tunnel through it.
