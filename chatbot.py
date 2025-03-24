import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# setting the environment
load_dotenv()
CHROMA_PATH = "chroma_db"

# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Get the collection
collection = chroma_client.get_or_create_collection(name="data")

# Initialize OpenAI client for generating embeddings
client = OpenAI()

# OpenAI's embedding model (this model provides embeddings of size 384)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")  # Using text-embedding-ada-002 (384-dimensional)

# Function to handle user queries
def handle_query(user_query):
    try:
        # Create embedding for the user query
        user_query_embedding = embeddings.embed_query(user_query)

        # Search for relevant answers in ChromaDB
        results = collection.query(
            query_embeddings=[user_query_embedding],
            n_results=1
        )

        # If no relevant results are found, return a default message
        if len(results['documents']) == 0:
            return "Det ved jeg desværre ikke."

        # Create system prompt for OpenAI model
        system_prompt = """
        You are a helpful assistant. You answer questions based on knowledge I provide you.
        You don't use your internal knowledge and you don't make things up.
        If you don't know the answer, just say that.
        --------------------
        The data:
        """ + str(results['documents']) + """
        """

        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Fejl: {e}")
        return "Der skete en fejl."

# Loop to keep the program running for multiple questions
while True:
    user_query = input("\n\nDatamatiker praktik chatbot. Hvad kan jeg hjælpe med?\n\n")
    
    if user_query.lower() in ['exit', 'quit', 'stop', 'afslut', 'luk']:
        print("Chatbotten lukkes.")
        break
    
    # Get the response from the model
    response = handle_query(user_query)
    
    print("\n\n---------------------\n\n")
    print(response)
