import psycopg2
from langgraph import Agent, Graph
import spacy
from transformers import    pipeline
conn = psycopg2.connect(
    dbname='products',
    user = 'root',
password = 'root',
       host = 'local host',
       port = '3306'
)
cursor = conn.cursor()

nlp = spacy.load('en_core_web_sm')
summarizer = pipeline('summarization', model="facebook/bart-large-cnn")
def query_database(query):
    cursor.execute(query)
    return cursor.fetchall()

def parse_user_input(user_input):
    doc = nlp(user_input)
    keywords = [token.text.lower() for token in doc if token.is_alpha]

    if "supplier" in keywords:
        return "SELECT * FROM suppliers;"
    elif "product" in keywords:
        return "SELECT * FROM products;"
    else:
        return None

def summarize_results(results):
    data_str = "\n".join([str(row) for row in results])
    summary = summarizer(data_str, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']

agent = Agent()
def handle_query(message):
    user_input = message['content']
   db_query =parse_user_input(user_input)
if db_query:
    results = query_database(db_query)
    summary = summarize_results(results)
    return {"content" : summary}
else
    return {"content" : "Sorry, I didn't understand your request. Please mention 'product' or 'supplier'."}

graph = Graph(agent)
graph.add_route("/start" "/query")
user_message = {"content": "Show me all products"}
response = graph.run("/start", user_message)
print(response['content'])