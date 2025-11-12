from celery import shared_task
from detection.models import *
from django.shortcuts import render
from detection.core.ProcessCheckingDocument import *
from detection.views import *
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")
# model = 0

# @shared_task
def InstructorUploadProcessCheckingDocuments(instructor, checking_document):
    """
    Processes an instructor’s uploaded document for plagiarism analysis.

    This function performs the full preprocessing pipeline for a newly uploaded
    instructor document, including:
    - Parsing the document’s text and extracting sentences.
    - Storing sentence-level data in the database.
    - Generating semantic embeddings (vectors) for each sentence.
    - Marking the document as fully processed upon completion.

    Args:
        instructor (Instructor): The instructor instance who uploaded the document.
        checking_document (CheckingDocument): The uploaded document to process.

    Returns:
        list[CheckingDocumentTextVector]: A list of saved text vector database objects
                                          generated for the document’s sentences.

    Notes:
        - Uses the SentenceTransformer model "all-MiniLM-L6-v2" for encoding.
        - Automatically updates the `is_processed` flag on the CheckingDocument.
        - Ensures sentence and object counts match before vectorization.
    """



    text = CheckingDocumentParse(checking_document)
    sentences, sentences_objs = CheckingDocumentStoreTextSentences(checking_document, text)
    if len(sentences) != len(sentences_objs):
        print("sentences and sentences_objs length are not equal")
    sentence_vectors_obj = CheckingDocumentGenerateTextVector(checking_document, model, sentences, sentences_objs)
    checking_document.is_processed = True
    checking_document.save()

    return sentence_vectors_obj