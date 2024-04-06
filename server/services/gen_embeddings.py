from nomic import embed

def generate_embeddings(text: str):    
    embeddings_responses = embed.text(
        texts=[text],
        model='nomic-embed-text-v1.5',
        task_type='search_document',
        dimensionality=512,
    )
    
    vectors = embeddings_responses['embeddings'][0]
    
    return vectors