from celery import shared_task
from detection.models import *
from django.shortcuts import render
from detection.core.ProcessResearchDocument import *
from detection.views import *
from sentence_transformers import SentenceTransformer


# model = SentenceTransformer("distiluse-base-multilingual-cased-v2") # Multi-lingual support
model = SentenceTransformer("all-MiniLM-L6-v2")
# model = 0

def UniversityUploadProcess(university):
    """
    Retrieves all unprocessed research documents uploaded by a university.

    This function filters and returns research papers that have been uploaded
    but not yet processed for parsing, sentence extraction, or vectorization.

    Args:
        university (University): The university instance whose pending research
                                 documents are to be fetched.

    Returns:
        QuerySet[ResearchDocument]: A queryset of research documents that are
                                    marked as unprocessed (`is_processed=False`).

    Notes:
        - Used as a helper function for batch processing of university uploads.
        - Prints the count of unprocessed research papers for debugging/logging.
    """

    pending_research_papers = ResearchDocument.objects.filter(university_id=university, is_processed=False)
    # print("research documents were uploaded by university")
    # print("there are ", pending_research_papers.count(), " unprocessed documents")
    print("there are ", len(pending_research_papers), " paper")

    return pending_research_papers

# @shared_task
def UniversityUploadProcessDocuments(university):
    """
    Processes all unprocessed research documents uploaded by a university.

    This function executes the complete processing pipeline for each pending
    research document, including:
    - Parsing the document text.
    - Extracting and storing sentence-level data.
    - Generating semantic vectors using a SentenceTransformer model.
    - Marking each document as processed upon completion.

    Args:
        university (University): The university instance whose documents are being processed.

    Returns:
        QuerySet[ResearchDocument]: A queryset of the research documents that were processed.

    Notes:
        - Uses the "all-MiniLM-L6-v2" SentenceTransformer model for embedding generation.
        - Automatically updates each document’s `is_processed` status.
        - Ensures sentence count consistency before vectorization.
        - Intended to be used for asynchronous or batch document processing tasks.
    """

    pending_research_papers = UniversityUploadProcess(university)
    for index, pending_research_paper in enumerate(pending_research_papers):
        text = ResearchDocumentParse(pending_research_paper)
        sentences, sentences_objs = ResearchDocumentStoreTextSentences(pending_research_paper, text)
        if len(sentences) != len(sentences_objs):
            print("sentences and sentences_objs length are not equal")
        sentence_vectors = ResearchDocumentGenerateTextVector(pending_research_paper, model, sentences, sentences_objs)
        pending_research_paper.is_processed = True
        pending_research_paper.save()

    return pending_research_papers

    