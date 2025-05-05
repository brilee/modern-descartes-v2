system_prompt=$(cat <<EOF

---------------------

Nitpick this essay for basic grammatical issues. Additionally, evaluate against these guidelines:
- Favor shorter, direct, active sentence structures.
- Eliminate adjectives and complex words when a simpler word suffices.
- Avoid idioms or analogies rooted in a particular culture, e.g. generational slang, American-isms, tech bro.
- Avoid tangents that do not contribute to the core thesis of the essay.

If any of these guidelines are not met, state the unmet guideline, excerpt the portion of the essay that violates the guideline, and suggest a revised version that would satisfy the guidelines.

)

cat $1 | llm -s "$system_prompt" -m openrouter/anthropic/claude-3.5-sonnet -u