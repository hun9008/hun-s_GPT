import ollama

response = ollama.chat(model='llama3:8b', messages = [
    {
        'role': 'user',
        'content': 'explane backpropagation.',
    },
])

print(response['message']['content'])