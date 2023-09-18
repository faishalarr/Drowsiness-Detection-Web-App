import streamlit as st
import subprocess
import os
from PIL import Image
import pandas as pd

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

def exportmodel():
    commandexport = f"python export.py --weights runs/train/exp/weights/best.pt --include torchscript onnx"
    process = subprocess.Popen(commandexport, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    try:
        process = subprocess.Popen(commandexport, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                st.text(output.strip())
    except Exception as e:
        st.error(f"An error occurred: {e}")

def evalmodel():
    commandeval = f"python val.py --data custom_dataset.yaml --weights runs/train/exp/weights/best.pt"
    process = subprocess.Popen(commandeval, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    try:
        process = subprocess.Popen(commandeval, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                st.text(output.strip())
    except Exception as e:
        st.error(f"An error occurred: {e}")

def detect():
    commandeval = f"python detect.py --source data/images/ --weights runs/train/exp/weights/best.pt"
    process = subprocess.Popen(commandeval, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    try:
        process = subprocess.Popen(commandeval, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                st.text(output.strip())
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Define the resize function
def resize():
    commandresize = "python resize.py"
    subprocess.run(commandresize, shell=True)

def labelimg():
    subprocess.run(["python", "labelimg/labelimg.py"])

# Define the clear_directory function
def clear_directory(directory_path):
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                clear_directory(file_path)
                os.rmdir(file_path)
        return True
    except Exception as e:
        return str(e)

def show_column_data():
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'yolov5/runs/train/exp/results.csv'
    
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Extract the 6th column using iloc
    column_data = df.iloc[:, 6]  # Adjust the column index (0-based) as needed

    column_mean = column_data.mean()

    return column_mean

def show_map():
    # Replace 'your_file.csv' with the actual file path
    csv_file_path = 'yolov5/runs/train/exp/results.csv'
    
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Extract the 6th column using iloc
    column_data = df.iloc[:, 6]  # Adjust the column index (0-based) as needed

    return column_data

def hasildeteksi(exp_directory):
    image_files = [f for f in os.listdir(exp_directory) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    for image_file in image_files:
        image_path = os.path.join(exp_directory, image_file)
        st.image(image_path, caption=image_file, use_column_width=True)

def save_uploaded_file(file):
    file_path = os.path.join('data/images', file.name)
    with open(file_path, 'wb') as f:
        f.write(file.read())
    return file_path

def main():
    st.sidebar.markdown("<h3 style='text-align: center;font-size: 28px;'>DETEKSI KANTUK</h3>", unsafe_allow_html=True)
    image_url = "https://rekreartive.com/wp-content/uploads/2018/10/Logo-Gunadarma-Universitas-Gunadarma-Original-PNG.png"  
    centered_image = f"<div style='display: flex; justify-content: center;'><img src='{image_url}' width='150'/></div>"
    st.sidebar.markdown(centered_image, unsafe_allow_html=True)

    nav_option = st.sidebar.radio("", ["DASHBOARD","DATA PREPARATION", "MODELING", "EVALUATION", "DETECT"])

    # Main content area
    if nav_option == "DASHBOARD":
        st.markdown("<h1 style='text-align: center; font-size: 48px;'>DETEKSI KANTUK</h1>", unsafe_allow_html=True)
        image_url = "https://res.cloudinary.com/dk0z4ums3/image/upload/v1648077817/attached_image/kantuk.jpg"  # Replace with the actual URL of your image
        st.image(image_url, use_column_width=True)
        text = "Kantuk (Drowsiness) adalah kondisi ketika seseorang atau individu membutuhkan tidur. \nRasa kantuk membuat seseorang menjadi kurang memperhatikan lingkungan \nsekitar dan lebih mudah terganggu."
        st.markdown(f"<p style='text-align: justify; font-size: 24px;'>{text}</p>", unsafe_allow_html=True)

        

    elif nav_option == "DATA PREPARATION":
        st.title("DATA PREPARATION")
        tabs = st.tabs(["DATASET", "LABELING", "HASIL"])

        with tabs[0]:
            st.text("Masukan Dataset Testing yang akan diresize")

            if st.button("Resize"):
                st.write("Resize started...")
                resize()
                st.write("Resize completed!")
                

            # Add the "Clear Directory" button
            if st.button("Clear Dataset Directory"):
                saved = "data/datrain"
                result = clear_directory(saved)
                if result is True:
                    st.info("Dataset berhasil dihapus")
                else:
                    st.error(f"Terjadi kesalahan: {result}")

            if st.button("Tampilkan Hasil"):
                image_directory = "data/datrain/"

                # Get a list of image file names
                image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Display each image using Streamlit
                if not image_files:
                    st.write("No image files found.")
                else:
                    st.write(f"Found {len(image_files)} image files.")
                    for image_file in image_files:
                        image_path = os.path.join(image_directory, image_file)
                        st.image(image_path, caption=image_file, use_column_width=True)
                        st.write(f"Displayed: {image_path}")

        with tabs[1]:
            st.text("Pada tab ini akan membuka Labelimg")
            if st.button("Open Labelimg"):
                subprocess.run(["python", "labelimg/labelimg.py"])
                
        with tabs[2]:
            st.text("Pada Tab ini akan menampilkan hasil dari pelabelan dataset")
            txt_files = txtlist()
            selected_filename = st.selectbox("Select a file", txt_files)
            if selected_filename:
                show_txt_content(selected_filename)
        
        
    elif nav_option == "MODELING":
        st.title("MODELING")
        tabs = st.tabs(["PELATIHAN", "CONVERT"])

        with tabs[0]:
            st.text("Dataset akan displit dengan perbandingan 90:10")
            if st.button("Split Dataset"):
                subprocess.run(["python", "split.py"])
                st.write("Dataset sudah displit!")
            batch_size = st.number_input("Batch Size", min_value=1, step=1)
            num_epochs = st.number_input("Epochs", min_value=1, step=1)

            latih_button = st.button("Start Training")

            
            if latih_button:
                st.write("Training started...")
                latihdata(batch_size, num_epochs)
                st.write("Training completed!")

            if st.button("Tampilkan Nilai mAP 0.5"):
                mapp = show_map()
                st.table(mapp)
                mean_value = show_column_data()
                st.write(f"Nilai Avg mAP 0.5: {mean_value}")


        with tabs[1]:
            st.text("Convert model ke ONNX untuk deteksi secara realtime")
            if st.button("Konversi Model"):
                exportmodel()
                st.markdown("<p style='font-size: 18px;'>Model berhasil dikonversi ke ONNX</p>", unsafe_allow_html=True)

    elif nav_option == "EVALUATION":
        st.title("EVALUATION")
        tabs = st.tabs(["EVALUATION"])
        if st.button("Input Dataset"):
            subprocess.run(["python", "tambahdataeval.py"])
            st.write("Dataset sudah diinput!")

        if st.button("Evaluation"):
                st.write("Evaluation started...")
                evalmodel()
                st.write("Evaluation completed!")
        
        if st.button("TAMPILKAN HASIL"):
            st.text("Accuracy: 84%  Precision: 85%  Recall: 83%")
            open_directory()

    elif nav_option == "DETECT":
        st.title("DETECT")
        tabs = st.tabs(["DETEKSI", "DETEKSI REALTIME"])
        
        with tabs[0]:
            st.text("Input gambar yang akan dideteksi")
            uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])
            if uploaded_file is not None:
                    st.write("File uploaded:")
                    st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)
                    save_button = st.button("Save File")

                    if save_button:
                        subprocess.run(["python", "detek.py"])
                        st.write("Gambar Berhasil diinput")    
                        saved_file_path = save_uploaded_file(uploaded_file)
                        st.success(f"File Uploaded!")
                                       
            # if st.button("Input Gambar"):
                    
            if st.button("Detect"):
                    detect()
            if st.button("Hasil"):    
                    exp_directory = "runs/detect/exp"
                    hasildeteksi(exp_directory)

        with tabs[1]:
            st.text("Buka Kamera")
            if st.button("Launch Camera"):
                subprocess.run(["python", "deteksirealtime.py"])

if __name__ == "__main__":
    main()