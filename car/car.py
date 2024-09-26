from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('car.html')
    
# Run the app using an asyncio event loop
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
