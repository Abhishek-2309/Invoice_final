from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface.llms import HuggingFacePipeline
import torch

model_id = "Qwen/Qwen3-4B"

llm_model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")
llm_tokenizer = AutoTokenizer.from_pretrained(model_id)

hf_pipe = pipeline("text-generation", model=llm_model, tokenizer=llm_tokenizer, max_new_tokens=4096, return_full_text=False)
llm = HuggingFacePipeline(pipeline=hf_pipe)
