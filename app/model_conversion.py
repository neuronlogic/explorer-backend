import os
import json
import sys
import logging
import requests
import pandas as pd
import torch
import torch.onnx

def convert_models_to_onnx(json_file, nsga_net_path, logs_path, files_path):
    """
    Converts models to ONNX format from a list of models specified in a CSV file.

    Parameters:
    - csv_file (str): Path to the CSV file containing model uids and Hugging Face account names.
    - nsga_net_path (str): Path to the NSGA-Net directory.
    - logs_path (str): Path where logs will be saved.
    - files_path (str): Path where model files will be saved.

    Returns:
    - None
    """
    # Ensure paths and logging
    if os.path.exists(nsga_net_path):
        sys.path.insert(0, nsga_net_path)
    else:
        logging.warning(f"Path {nsga_net_path} does not exist. Ensure the path is correct.")

    logging.basicConfig(
        filename=os.path.join(os.makedirs(logs_path, exist_ok=True) or logs_path, 'model_conversion.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    with open(f'{json_file}', 'r') as f:
        json_data = json.load(f)
    # Read the CSV file
    df = pd.DataFrame(json_data['data'], columns=json_data['columns'])
    uids_and_hf_accounts = df[['uid', 'hf_account']]

    def load_model(model_dir):
        try:
            model = torch.jit.load(model_dir, map_location=torch.device('cpu'))
            logging.info("Torch script model loaded using torch.jit.load")
            return model
        except Exception as e:
            logging.warning(f"torch.jit.load failed with error: {e}")
            try:
                model = torch.load(model_dir, map_location=torch.device('cpu'))
                logging.info("Model loaded using torch.load")
                return model
            except Exception as jit_e:
                logging.error(f"torch.load also failed with error: {jit_e}")
                raise

    # Iterate over each model to download and convert
    for row in uids_and_hf_accounts.itertuples(index=False):
        try:
            url = f'https://huggingface.co/{row.hf_account}/resolve/main/model.pt'
            logging.info(f"Attempting to download model from {url}")

            response = requests.get(url)
            if response.status_code == 200:
                model_file = os.path.join(os.makedirs(files_path, exist_ok=True) or files_path, f'{row.uid}.pt')
                with open(model_file, 'wb') as f:
                    f.write(response.content)
                logging.info(f"Model {row.uid} downloaded successfully.")
            else:
                raise Exception(f"Failed to download model. Status code: {response.status_code}")

            model = load_model(model_file)
            logging.info(f"Model {row.uid} loaded successfully.")

            # Ensure the model is in evaluation mode and on the CPU
            model.eval()
            model.to('cpu')  # Ensure the model is on the CPU

            dummy_input = torch.randn(1, 3, 32, 32).to('cpu')  # Ensure the dummy input is on the CPU

            # Set the path for the ONNX model
            onnx_path = f"{files_path}/{row.uid}.onnx"

            # Export the model to ONNX
            torch.onnx.export(model,             # model being run
                              dummy_input,       # model input (or a tuple for multiple inputs)
                              onnx_path,         # where to save the model (can be a file or file-like object)
                              export_params=True,  # store the trained parameter weights inside the model file
                              opset_version=12,    # the ONNX version to export the model to
                              do_constant_folding=True,  # whether to execute constant folding for optimization
                              input_names=['input'],   # the model's input names
                              output_names=['output'],  # the model's output names
                              dynamic_axes={'input' : {0 : 'batch_size'},    # variable length axes
                                            'output' : {0 : 'batch_size'}})

            logging.info(f"Model {row.uid} has been converted to ONNX format at {onnx_path}")
        except Exception as e:
            logging.error(f"An error occurred for model {row.uid}: {e}")

