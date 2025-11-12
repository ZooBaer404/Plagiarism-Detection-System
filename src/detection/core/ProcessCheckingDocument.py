import fitz # pymupdf
import numpy as np
import io
from django.core.files.base import ContentFile
from detection.models import *
import re
from nltk.tokenize import sent_tokenize

## CheckingDocument Processing

def CheckingDocumentParse(document: CheckingDocument):
    """
    Extracts and analyzes content from the given document, including text, images, and references.

    This function processes a PDF document to:
    - Extract all textual content across all pages.
    - Detect and save embedded images.
    - Compute key document statistics (pages, words, sentences, characters, references, etc.).
    - Identify and separate the 'References' section from the main text.
    - Store parsed text, reference entries, and statistical data in respective database models.

    Args:
        document (CheckingDocument): The document object containing metadata and file reference.

    Returns:
        str: The original text content of the document (excluding the 'References' section).
        Returns an empty string if no 'References' section is found.

    Notes:
        - Relies on PyMuPDF (fitz) for PDF parsing.
        - Saves multiple related objects (images, references, statistics, parsed text) to the database.
        - Handles and logs errors when a 'References' section is missing.
    """

    no_of_pages = 0
    no_of_words = 0
    no_of_characters = 0
    no_of_sentences = 0
    no_of_references = 0
    size_of_document = 0
    no_of_images = 0
    images_list = list()
    find_references_word = "references"
    find_references_index = -1
    reference_text = ""
    original_text = ""

    text = ""
    doc_pdf = fitz.open(document.checking_document_file.path)

    for page_number, page in enumerate(doc_pdf):
        image_list = page.get_images(full=True)

        for img_index, image_tuple in enumerate(image_list):

            xref = image_tuple[0]
            base_image = doc_pdf.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_file = ContentFile(image_bytes)

            filename = f"page_{page_number+1}_img_{img_index+1}.{image_ext}"

            checking_document_images_obj = CheckingDocumentImages()
            checking_document_images_obj.checking_document_id = document
            checking_document_images_obj.image.save(filename, image_file, save=False)
            checking_document_images_obj.save()

        num_images_on_page = len(image_list)
        no_of_images += num_images_on_page
        images_list.append(image_list)
        no_of_pages += 1

        temp = page.get_text("text")
        text += temp

    # print("Document is ", text)

    no_of_words = len(text.split())
    no_of_characters = len(text)
    # no_of_sentences = len(re.split(r'[.\n!?]+', text))
    size_of_document = document.checking_document_file.size    

    find_references_index = text.lower().rfind(find_references_word.lower())
    # print("last references found in ", find_references_index)

    if find_references_index == -1:
        error_obj = CheckingDocumentParseError()
        error_obj.checking_document_id = document
        error_obj.parse_text = text
        error_obj.error_message = "There are no References section in the checking paper"
        error_obj.save()
        return ""
    else:
        reference_text = text[find_references_index:]
        original_text = text[:find_references_index]

    # finding_references_list = re.split(r"\n[\{][0-9]+[\}]", reference_text)
    finding_references_list = re.split(r"\n\n", reference_text)

    print("there ", len(finding_references_list), " references")
    no_of_sentences = len(sent_tokenize(original_text))


    document_basic_stats_obj = CheckingDocumentBasicStats()
    document_basic_stats_obj.checking_document_id = document
    document_basic_stats_obj.size_of_document = size_of_document
    document_basic_stats_obj.no_of_sentences = no_of_sentences
    document_basic_stats_obj.no_of_words = no_of_words
    document_basic_stats_obj.no_of_characters = no_of_characters
    document_basic_stats_obj.no_of_images = no_of_images
    document_basic_stats_obj.no_of_references = len(finding_references_list)
    document_basic_stats_obj.save()

    for index, reference_text in enumerate(finding_references_list):
        document_reference_obj = CheckingDocumentReferences()
        document_reference_obj.checking_document_id = document
        document_reference_obj.index = index
        document_reference_obj.reference_text = reference_text
        print("reference length is ", reference_text)
        document_reference_obj.save()

    document_parse_text_obj = CheckingDocumentParseText()
    document_parse_text_obj.checking_document_id = document
    document_parse_text_obj.parse_text = original_text
    document_parse_text_obj.save()


    print("orignal: ", original_text)
    print("reference: ", reference_text)

    return original_text

def CheckingDocumentGetSentencesFromText(document_extracted_text):
    """
    Splits the extracted document text into individual sentences using NLP-based tokenization.

    Args:
        document_extracted_text (str): The full text extracted from the document.

    Returns:
        list[str]: A list of sentences derived from the input text.

    Notes:
        - Utilizes NLTK's `sent_tokenize` for more accurate sentence segmentation.
        - Filters out unnecessary whitespace and empty entries.
    """

    # # Split on .\n, or !, ?, or newline not preceded by period
    # sentences = re.split(r'\.\n|[!?]\s+|(?<!\.)\n', document_extracted_text)
    # # Clean and filter
    # sentences = [s.strip() for s in sentences if s.strip()]
    # return sentences

    # More Accurate one
    sentences = sent_tokenize(document_extracted_text)
    return sentences

def CheckingDocumentStoreTextSentences(document, document_extracted_text):
    """
    Stores each sentence from the extracted text as a separate database record.

    This function tokenizes the document text into sentences, creates individual
    `CheckingDocumentEnhancedText` entries for each, and stores them with index tracking.

    Args:
        document (CheckingDocument): The document object being processed.
        document_extracted_text (str): The text content extracted from the document.

    Returns:
        tuple[list[str], list[CheckingDocumentEnhancedText]]:
            - List of extracted sentences.
            - List of corresponding saved database objects.

    Notes:
        - Useful for later NLP or semantic vectorization steps.
        - Prints progress logs showing the number of sentences saved.
    """

    sentences = CheckingDocumentGetSentencesFromText(document_extracted_text)
    sentences_objs = list()

    for index, sentence in enumerate(sentences):
        document_enhanced_text_obj = CheckingDocumentEnhancedText()
        document_enhanced_text_obj.checking_document_id = document
        document_enhanced_text_obj.sentence_index = index
        document_enhanced_text_obj.sentence_enhanced_text = sentence
        document_enhanced_text_obj.save()
        sentences_objs.append(document_enhanced_text_obj)

    print("info: Document's text stored successfully")
    print("There are ", len(sentences_objs), " sentences")
    return sentences, sentences_objs


def CheckingDocumentGenerateTextVector(document, model, sentences, sentences_objs):
    """
    Generates and stores semantic vector representations for each sentence in the document.

    This function uses a provided NLP embedding model (e.g., SentenceTransformer)
    to encode sentences into vector representations, which are then stored in
    the `CheckingDocumentTextVector` model linked to their corresponding text entries.

    Args:
        document (CheckingDocument): The document object being processed.
        model: The text embedding model used to generate sentence vectors.
        sentences (list[str]): The list of sentences to be vectorized.
        sentences_objs (list[CheckingDocumentEnhancedText]): Corresponding database objects for each sentence.

    Returns:
        list[CheckingDocumentTextVector]: A list of saved text vector database objects.

    Notes:
        - Each sentence vector is stored as a list (converted from NumPy array or tensor).
        - Ensures one-to-one mapping between sentence text and vector.
        - Prints debugging info including number of generated vectors.
    """

    sentences_vectors = model.encode(sentences)
    sentences_vectors_obj = list()

    print("vectors: ", sentences_vectors, "\n\n")

    for index, sentences_vector in enumerate(sentences_vectors):
        checking_document_sentence_vector_obj = CheckingDocumentTextVector()
        checking_document_sentence_vector_obj.checking_document_id = document
        checking_document_sentence_vector_obj.checking_document_enhanced_text_id = sentences_objs[index]
        checking_document_sentence_vector_obj.text_vector = sentences_vector.tolist()
        checking_document_sentence_vector_obj.save()
        sentences_vectors_obj.append(checking_document_sentence_vector_obj)
    
    print("there are ", len(sentences_vectors_obj), " sentences objects")
    return sentences_vectors_obj

