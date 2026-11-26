# Local ComfyUI operations

The usual base URL is `http://127.0.0.1:8188`. Check that the server is available before starting a second instance. Find the existing launch command and environment instead of assuming a generic Python has every custom node's dependencies. Inspect `nvidia-smi` when resources are tight, and stop or unload another model only with the person's permission.

Read-only endpoints to inspect on the installed server:

- `GET /system_stats`: runtime and device details.
- `GET /queue`: `queue_running` and `queue_pending`. Entries include a prompt ID and a workflow. Summarize the counts first, and inspect only the relevant workflows when investigating stale work.
- `GET /history/{prompt_id}`: status, execution messages and saved outputs for that job.
- `GET /object_info` or `/object_info/{class_type}`: installed node schemas, enums and input types.

Submit API-format graphs with `POST /prompt` and the JSON body `{"prompt": GRAPH, "client_id": PROJECT_CLIENT_ID}`. Save the exact request to a versioned file before submitting. Afterwards save the `prompt_id`, the queue number, and any errors and node errors. Poll the specific job at sensible intervals. An empty queue alone is not success. Find the output files from the returned node outputs, resolving filename, subfolder and type under the configured output directory.

Endpoints that change state exist for deleting queue items and interrupting execution. Check how the installed version behaves before calling them. Remove only identified, obsolete job IDs, and only with permission. A broad queue clear can destroy other work.

## Reading a workflow

Node IDs are specific to one workflow file. In a typical reference-to-video graph you will find nodes like these, under whatever IDs that file uses:

- a reference-to-video node that holds the prompt and the reference connections
- a float or integer primitive that controls duration
- a noise node that holds the seed
- model loaders, which must name a checkpoint that is installed
- `LoadImage` and `LoadAudio` nodes, one pair for each reference
- a `SaveVideo` node that holds the filename prefix

Reference inputs can be named like `ref_images.ref_image_1` and `ref_audios.ref_audio_1`. Trace every connection back to its load node and work out which character it represents before you write the `<Picture N>` and `<Audio N>` assignments in the prompt.

A custom node that names a model shows only that the node is installed. It says nothing about that model's source, licence or official availability. Check those separately when it matters.
