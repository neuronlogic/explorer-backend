## Backend Server for Model Visualizer

### Project Initialization

We are currently using a simple file server for our model visualizer. The backend server is initialized with Flask, and we plan to transition to using Flask for a more robust solution in the future.

### Installation and Setup

1. **Create a Virtual Environment**

   To manage dependencies, create a virtual environment using Python 3:

   ```bash
   python3 -m venv .venv
   ```

2. **Activate the Virtual Environment**

   Activate the virtual environment with the following command:

   ```bash
   . .venv/bin/activate
   ```

3. **Install Dependencies**

   Install the required dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```
### Downloading and Converting the Model

To download and convert the model, execute the following script:

```bash
python app/download.py
```

### Running the Server

To run the server, execute:

```bash
cd app
python server.py
```

### Running the Server with PM2 [Optional]

For background process management, use PM2:

```bash
cd app
pm2 start --name="explorer-backend" server.py
```


### Notes

- Ensure that you have the necessary dependencies installed and paths correctly set up before running the script.
- For detailed logging and debugging, refer to the `model_conversion.log` file located in the `./logs` directory.
- For long-term use, consider configuring PM2 to manage the server's lifecycle, including automatic restarts and monitoring.
