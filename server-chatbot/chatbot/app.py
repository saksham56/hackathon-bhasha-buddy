from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os
import time
import logging
from datetime import datetime
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app)
# CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
CORS(app, supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'])

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"
assistant_id = "asst_ykEnY7XvIO6dh1SWBI9VjIzY"
thread_id = "thread_dcXB2Ixmh680M4lgMC9GPVMy"

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                return response
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    message_text = data.get('message')
    if not message_text:
        return jsonify({'error': 'No message provided'}), 400
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=message_text
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        response = wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5006)

