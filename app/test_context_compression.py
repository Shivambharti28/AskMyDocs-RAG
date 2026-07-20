from app.services.retrieval.context_compression import compress_chunk

chunk = """
Motivation is the process that initiates,
guides and maintains goal-directed behavior.

There are many theories.

Maslow proposed...

History...

Applications...

Conclusion...
"""

print(
    compress_chunk(
        "What is motivation?",
        chunk,
    )
)
