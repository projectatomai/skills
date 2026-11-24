---
name: agent-council
description: Convene Claude, Codex and Gemini for independent recommendations, a challenge round and an evidence-checked decision. Use when the user requests Agent Council or a three-provider review.
---

# Agent Council

Use the current session as coordinator. The other two providers participate through the user's authorized connections. The skill supplies the review procedure. Each participant needs its own working connection.

For each provider, use the strongest model the connected account exposes for the task and select **High** reasoning effort for both rounds. If High is part of the model ID, choose that variant. Check the current model options and verify the runtime model and effort. If the host is on a different configuration, use a fresh High session for its seat. Honor explicit overrides and report any seat that could not run as requested.

1. Write the decision, scope, evidence, constraints and a practical test. Record your own initial position before seeing the other answers. Remove personal details, secrets and unrelated workspace information from the brief.
2. Send the same brief independently to both peers. For example, if the host is Codex, ask Claude and Gemini. Use an available peer-consultation tool or a signed-in client the user authorized. Request a recommendation, its strongest objection and a test. Tell peers to answer in text, without tool use or further delegation.
3. Record which providers actually answered and the model identifiers their runtimes report. Honor a requested model. If a connection fails, retry it once and report missing participation. When peer connections are unavailable, give the user the brief to take to those clients. Only attribute an answer to a provider that returned one.
4. Compare the three answers, including the host's. Send both peers the same short synthesis, the proposed decision and any material disagreement. Ask each what would change the decision. If they identify a checkable claim, verify it with a primary source or a test.
5. Deliver the recommendation, the reason, meaningful dissent and the verification result. Identify anything still uncertain. Preserve the original scope of authorization for actions such as publishing or deployment.

## Try it

Ask: “Use Agent Council to choose whether a weekly report should be generated on demand or prepared every Monday. It takes 20 seconds to run and only some teams open it. Give me one decision and the measurement that would make you change it.”

A useful result explains what each participant contributed, which fact decided the question, and how the team can check it. Agreement alone is weak evidence.
