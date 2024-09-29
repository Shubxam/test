# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install git and git-lfs
RUN apt-get update && apt-get install -y git git-lfs

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run fetch-data.py and dashboard-generation.py when the container launches
CMD ["sh", "-c", "git lfs install && \
    GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis && \
    mkdir models && mv distilroberta-finetuned-financial-news-sentiment-analysis/ models/ && \
    cd models/distilroberta-finetuned-financial-news-sentiment-analysis/ && \
    git lfs pull --include model.safetensors && \
    cd ../../ && \
    python main.py"]