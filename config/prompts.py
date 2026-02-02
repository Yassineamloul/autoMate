"""Prompt templates for agents."""

INGEST_SYSTEM = "You are a document ingestion assistant. Extract text and metadata." 
SEGMENTER_PROMPT = "Split the document text into coherent policy chunks." 
RULE_EXTRACTION_PROMPT = "Given a chunk of policy text, extract any rules and obligations." 
OPPORTUNITY_PROMPT = "Given rules, suggest opportunity cards for automation." 
