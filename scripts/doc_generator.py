from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.mapreduce import MapReduceDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from config.settings import get_prompt_template_for_task

def run_scalable_doc_generation(llm: BaseChatModel, project_path: str) -> str:
    loader = DirectoryLoader(
        project_path, 
        glob="**/*.*", # More inclusive glob
        loader_cls=TextLoader, 
        recursive=True, 
        show_progress=True,
        use_multithreading=True,
        silent_errors=True
    )
    docs = loader.load()
    
    if not docs:
        return "No documents found in the specified path."

    map_prompt = get_prompt_template_for_task("docs_map")
    map_chain = LLMChain(llm=llm, prompt=map_prompt)

    reduce_prompt = get_prompt_template_for_task("docs_reduce")
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="doc_summaries"
    )

    map_reduce_chain = MapReduceDocumentsChain(
        llm_chain=map_chain,
        reduce_documents_chain=combine_documents_chain,
        document_variable_name="page_content",
        return_intermediate_steps=False,
    )

    # Split documents to respect context window on map step
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(docs)

    result = map_reduce_chain.invoke(split_docs)
    return result.get("output_text", "Failed to generate documentation.")
