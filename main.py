from agent.graph import agent

response = agent.invoke({
    "messages": [
        {"role": "user", "content": "Why are deliveries getting delayed?"}
    ]
})

print(response)