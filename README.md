## Backend Server for Model Visualizer

### Project Initialization

We are currently using FastAPI for our model visualizer, providing a lightweight and efficient backend. This allows for handling asynchronous tasks and better performance for API requests. While FastAPI is serving our needs at the moment, we are planning to transition to Flask in the future to implement a more robust and feature-rich solution as our project scales.

### Installation and Setup

1. **Create a Virtual Environment**

   To manage dependencies, create a virtual environment using Python 3:

   ```bash
   python3 -m venv .venv
   ```

2. **Activate the Virtual Environment**

   Activate the virtual environment with the following command:

   ```bash
   source .venv/bin/activate
   ```

3. **Install Dependencies**

   Install the required dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```
4. **Setting Env environment**

   ```bash
   cp .env.sample .env
   ```
### Running the development Server

To run the server, execute:

```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8081
```

### Running the Server with PM2 [Optional]

For background process management, use PM2:

```bash
cd app
pm2 start --name="explorer-backend" start.sh
```

### Running the Server with gunicorn for Production

You can start your FastAPI app with gunicorn using the UvicornWorker like this:

```bash
cd app
gunicorn -k uvicorn.workers.UvicornWorker main:app --workers 4 --bind 0.0.0.0:8081
```

### Notes

- Ensure that you have the necessary dependencies installed and paths correctly set up before running the script.
- For detailed logging and debugging, refer to the `model_conversion.log` file located in the `./logs` directory.
- For long-term use, consider configuring PM2 to manage the server's lifecycle, including automatic restarts and monitoring.
