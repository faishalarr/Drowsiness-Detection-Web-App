import streamlit as st
import subprocess
import os
from PIL import Image

def run_tambahtesting():
    val_images_dir = os.path.join("dataset", "images", "val")

    # Create the directory if it doesn't exist
    os.makedirs(val_images_dir, exist_ok=True)

    # Handle file upload
    uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    for uploaded_file in uploaded_files:
        file_contents = uploaded_file.read()

        # Determine the file path where you want to save the uploaded file
        save_path = os.path.join(val_images_dir, uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(file_contents)

    if uploaded_files:
        st.success("Files uploaded and saved successfully.")

def select_weights_directory():
    st.text("Running evaluation...")
    commandeval = f"python val.py --data custom_dataset.yaml --weights runs/train/exp/weights/best.pt"
    subprocess.run(commandeval, shell=True)
    st.text("Evaluation completed.")

def open_directory():
    dor_path = "runs/val/exp/"
    image_filea = [f for f in os.listdir(dor_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    st.image(os.path.join(dor_path, image_filea[0]))
    # Add logic for iterating through images

def txtlist():
    dor_path = "data/datrain/"  # Path to the directory containing .txt files
    txt_files = [f for f in os.listdir(dor_path) if f.lower().endswith('.txt')]
    return txt_files

def show_txt_content(filename):
    with open(os.path.join("data/datrain", filename), "r") as file:
        content = file.read()
        st.text("File Content:")
        st.code(content)

def latihdata(batch_size, num_epochs):
    commandtrain = f"python train.py --img 640 --batch {batch_size} --epochs {num_epochs} --data custom_dataset.yaml --weights yolov5s.pt --cache"
    process = subprocess.Popen(commandtrain, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    try:
        process = subprocess.Popen(commandtrain, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                st.text(output.strip())
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    st.title("DETEKSI KANTUK")

    # Create tabs
    tabs = st.tabs(["Input Dataset", "Evaluate Model", "Show Results", "Hasil Pelabelan", "Modeling"])

    # Input Dataset tab
    with tabs[0]:
        st.text("This tab is for inputting the dataset.")
        
        # Create subheader to simulate subtab choices
        subtab_option = st.subheader("Subtab options:")
        selected_subtab = subtab_option.radio("", ["Upload Images", "Other Options"])

        if selected_subtab == "Upload Images":
            run_tambahtesting()

        elif selected_subtab == "Other Options":
            st.write("Other options can go here.")
    with tabs[1]:
        st.text("This tab is for evaluating the model.")
        if st.button("EVALUASI MODEL"):
            select_weights_directory()

    # Show Results tab
    with tabs[2]:
        st.text("This tab is for showing the evaluation results.")
        if st.button("TAMPILKAN HASIL"):
            open_directory()

    with tabs[3]:
        st.text("Click a file name in the list to view its content.")
        txt_files = txtlist()
        selected_filename = st.selectbox("Select a file", txt_files)
        if selected_filename:
            show_txt_content(selected_filename)

    with tabs[4]:
        batch_size = st.number_input("Batch Size", min_value=1, step=1)
        num_epochs = st.number_input("Number of Epochs", min_value=1, step=1)

        latih_button = st.button("Start Training")

        if latih_button:
            st.write("Training started...")
            latihdata(batch_size, num_epochs)
            st.write("Training completed!")

if __name__ == "__main__":
    main()
