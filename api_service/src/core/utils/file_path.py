import os
import shutil
import uuid
from os import path


def dataset_file_path(instance, filename):
    extension = filename.split(".")[-1]
    unique_filename = f"{str(uuid.uuid4())}.{extension}"
    return path.join("topics", instance.topic.slug, "datasets", unique_filename)


def chunk_file_path(topic_slug):
    file_name = f"{topic_slug}.pkl"
    file_path = path.join(chunk_directory_path(topic_slug), file_name)
    return file_path


def chunk_directory_path(topic_slug):
    directory_path = path.join("../uploads", "topics", topic_slug, "chunks")
    os.makedirs(directory_path, exist_ok=True)
    return directory_path


def delete_topic_directory(topic_slug):
    directory_path = path.join("../uploads", "topics", topic_slug)
    shutil.rmtree(directory_path, ignore_errors=True)
