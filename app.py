from flask import Flask, render_template, request, jsonify
from data_loader import load_district_data, load_block_data, load_yearly_data, load_availability_data
from chatbot import Aquabot

app = Flask(__name__)

# Load all datasets at startup
district_data = load_district_data('up.csv')
block_data = load_block_data('up2.csv')
yearly_data = load_yearly_data('rechargefinal.csv')
availability_data = load_availability_data('availablefinal.csv')


# Check if data loading was successful before initializing the bot
if all(data is not None for data in [district_data, block_data, yearly_data, availability_data]):
    bot = Aquabot(district_data, block_data, yearly_data, availability_data)
else:
    print("FATAL: Could not load one or more data files. The chatbot cannot start.")
    bot = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    if bot is None:
        return jsonify({'answer': 'I am sorry, but I could not load the necessary data to function. Please check the server logs.'})

    user_message = request.json.get('message', '')
    response = bot.answer_question(user_message)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
