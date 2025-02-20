# PDF2BRAINROT: Transform PDFs into Engaging Brainrot Content 🧠😵‍💫

> ⚠️ The project is still in development. Please be patient and report any issues you encounter. ⚠️

## Yep, you can use this script to convert a PDF file to Brainrot content.

Tired of boring PDFs? Want to inject some chaotic energy into your documents? **PDF2BRAINROT** is here to help! This script takes your standard PDF files and transforms them into dynamic, attention-grabbing "Brainrot" content.

**What is "Brainrot Content"?**

Think short, fast-paced, visually stimulating videos designed to grab attention and keep it.  PDF2BRAINROT leverages text-to-speech and dynamic video editing to convert your PDF's text into this engaging format.  Imagine your PDF's content brought to life with:

* **AI-powered Voiceover:**  Using `kokoro`, your PDF's text is converted into an expressive audio voiceover.
* **Timestamped Audio:** `vosk` adds precise timestamps to the audio, allowing for synchronized video editing.
* **Dynamic Video Generation:** `moviepy` combines the text, timestamped audio, and potentially other visual elements (you can customize this!) to create a "Brainrot" video.

**Think:**  Imagine excerpts from your PDF presented as fast-paced, captioned videos perfect for sharing on social media or grabbing attention in a digital age.

## Features

* **PDF Text Extraction:**  Efficiently extracts text content from PDF files using `pymupdf`.
* **Text-to-Speech Conversion:**  Generates natural-sounding audio voiceovers from the extracted text using `kokoro`.
* **Audio Timestamping:** Precisely timestamps the generated audio using `vosk` for accurate synchronization in video editing.
* **Brainrot Video Generation:**  Utilizes `moviepy` to create dynamic videos incorporating the text, timestamped audio, and customizable visual elements (currently basic, but highly extensible!).
* **Easy to Use:** Simple command-line interface for quick conversion.
* **Customizable (Future Potential):** The script is designed to be extensible, allowing for future customization of video styles, visual elements, and "Brainrot" effects.

## Installation

Get ready to unleash the Brainrot! Follow these steps to set up the script:

**1. Create a Virtual Environment (Recommended)**

It's always a good idea to work in a virtual environment to keep your project dependencies isolated.

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate # On Linux/macOS
```

**2. Install Required Libraries**

Install the necessary Python libraries using pip. Make sure you are in your virtual environment.

```bash
pip install -r requirements.txt
```

**3. (Optional) Install PyTorch with CUDA Support (For Faster Processing)**

If you have an NVIDIA GPU with CUDA cores, installing PyTorch with CUDA support can significantly speed up processing, especially if you expand the script to include more advanced features in the future.

* **Check your CUDA Toolkit Version:**  Find out which CUDA Toolkit version you have installed on your system.
* **Visit the PyTorch Website:** Go to the [official PyTorch Get Started page](https://pytorch.org/get-started/locally/).
* **Select your Configuration:** Choose your PyTorch version, operating system, package manager (pip), Python version, and **CUDA version**.
* **Copy and Run the Installation Command:** PyTorch will provide you with the correct `pip3 install` command.

   **Example for Windows with CUDA 11.8:**

   ```bash
   pip3 install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu118](https://download.pytorch.org/whl/cu118)
   ```

**4. Install Vosk Model (Local Installation)**

Vosk requires a local model for speech recognition and timestamping. Download and install the English (US) model:

**Using PowerShell (Windows):**

```powershell
Invoke-WebRequest -Uri "[https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip)" -OutFile "vosk-model-en-us-0.22.zip"; Expand-Archive -Path "vosk-model-en-us-0.22.zip" -DestinationPath "." -Force; Remove-Item "vosk-model-en-us-0.22.zip"
```

**For other operating systems (Linux/macOS), you might need to use `wget` and `unzip`:**

```bash
wget [https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip)
unzip vosk-model-en-us-0.22.zip
rm vosk-model-en-us-0.22.zip
```

This will download the `vosk-model-en-us-0.22.zip` file, extract it, and place the `vosk-model-en-us-0.22` folder in your project directory.

**5. Font and Content**

You will need to use font and your choice of brainrot content and replace the following lines with your file path
```bash
BASE_VIDEO = "videoplayback.mp4"
FONT_PATH = "./Roboto-ExtraBold.ttf"
```

## Usage

Transform your PDFs into Brainrot with a single command!

```bash
python pdf2brainrot.py --source <path_to_your_pdf_file>
```

* **`<path_to_your_pdf_file>`:** Replace this with the actual path to the PDF file you want to convert. For example: `my_document.pdf` or `C:\Users\YourName\Documents\report.pdf`

**Processing Time:**

The script's execution time depends on the size and content of your PDF file.  Larger files with more text will naturally take longer to process due to text extraction, audio generation, and video creation.  For a PDF with about 200 lines of text it will take approximately an hour to complete the full process.  Please be patient!

**Output:**

The script will generate a Brainrot video in the same directory as the script, likely named after your PDF file (e.g., `my_document_brainrot.mp4`).

## Acknowledgements

We would like to extend our sincere gratitude to the following communities for providing the incredible tools and resources that made PDF2BRAINROT possible:

* **The Kokoro Community:** For developing `kokoro`, a fantastic tool for expressive text-to-speech generation. Your work is instrumental in bringing the voice to Brainrot content.
* **The Vosk Community:**  For creating `vosk`, a powerful and accurate speech recognition toolkit that enables precise audio timestamping. This is essential for creating synchronized and engaging videos.
* **The Python Community:**  For the rich and versatile Python ecosystem and the countless libraries that empower developers worldwide. PDF2BRAINROT is built upon the shoulders of giants in the Python community.

Thank you for your dedication and open-source contributions!

## Contributions and Help

**Want to contribute to PDF2BRAINROT?**

We welcome contributions to make this script even more brainrotting!  Here are some ways you can help:

* **Suggest new features:**  Have ideas for making the videos more dynamic or adding more "Brainrot" effects? Let us know!
* **Improve video styles:**  Experiment with different `moviepy` effects and video editing techniques to create even more engaging Brainrot visuals.
* **Add support for more languages:**  Expanding language support for text extraction, text-to-speech, and speech recognition would be a valuable contribution.
* **Bug fixes and code improvements:**  Found a bug or have a way to optimize the code? Pull requests are greatly appreciated!

**Need help or have questions?**

If you encounter any issues, have questions about using the script, or just want to share your Brainrot creations, please feel free to reach out!  You can:

* **Open an issue on the project's GitHub repository (if applicable).**  *\[Link to your repository here if you have one]*
* **Contact the script author directly at \[pramoda9.2.2004@gmail.com]**

We are excited to see what Brainrot content you create and how you might contribute to this project!

**Have fun creating some Brainrot!** 😵‍💫🎉