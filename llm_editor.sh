system_prompt=$(cat <<EOF

---------------------

Review this essay, evaluating against these guidelines:
- The essay should have a punchy, intriguing, possibly even clickbaity title that makes the reader want to know more.
- The introductory paragraph should explain why the reader should care about what the essay has to say.
- The introductory paragraph should explain what the essay's contents will be.
- The body of the essay should deliver on the title.
- The body of the essay should deliver on the introductory paragraph's claims.
- The essay should not have gaps in the logic or narrative flow.
- The essay should remain professional and neutral

If any of these guidelines are not met, state the unmet guideline, excerpt the portion of the essay that violates the guideline, and suggest a revised version that would satisfy the guidelines.

)

cat $1 | llm -s "$system_prompt" -m openrouter/anthropic/claude-3.5-sonnet -u