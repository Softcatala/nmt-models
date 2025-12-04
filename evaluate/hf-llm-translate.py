#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import datetime
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import Mistral3ForConditionalGeneration

# ----------------------------------------------------------
# CONFIG: Only full HF paths here
# ----------------------------------------------------------
MODELS = [
    "mistralai/Ministral-3-14B-Instruct-2512-BF16",
    "google/gemma-3-12b-it",
]

# ----------------------------------------------------------
# FLORES LANG PAIRS
# ----------------------------------------------------------
PAIR_LANGUAGES = {
    "en-ca": ["English", "Catalan"],
}

# ----------------------------------------------------------
# Helper functions
# ----------------------------------------------------------
def file_len(fname):
    if not os.path.isfile(fname):
        return 0
    with open(fname) as f:
        return sum(1 for _ in f)

def get_sacrebleu(reference_file, hypotesis_file):
    JSON_FILE = "bleu.json"
    cmd = f"sacrebleu {reference_file} -i {hypotesis_file} -m bleu > {JSON_FILE}"
    os.system(cmd)
    with open(JSON_FILE) as f:
        data = json.load(f)
    return f"{data['score']:0.1f}"

def save_model_bleu(model_id, scores):
    filename = f"{model_id}-bleu.json"
    with open(filename, "w") as f:
        json.dump(scores, f, indent=4)
    print(f"Saved BLEU results to: {filename}")

# ----------------------------------------------------------
# Translation for causal LLMs
# ----------------------------------------------------------
def llm_translate(model, tokenizer, text, src_lang, tgt_lang):
    prompt = (
        f"Translate the following text from {src_lang} to {tgt_lang}. Provide ONLY the translation:\n"
        f"{text}\n\n"
        f"Translation:"
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    if "Translation:" in decoded:
        return decoded.split("Translation:", 1)[1].strip()
    return decoded.strip()

# ----------------------------------------------------------
# Evaluation loop for one model
# ----------------------------------------------------------
def evaluate_model(model_path):
    # Deduce a simple model name from the HF path
    model_id = model_path.split("/")[-1]

    start_time = datetime.datetime.now()
    print("=" * 80)
    print(f"Evaluating model: {model_id}  ({model_path})")
    print("=" * 80)

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

    if 'stral' in model_path:
        model = Mistral3ForConditionalGeneration.from_pretrained(
            model_path,
            device_map="cpu",  # runs entirely on CPU
            quantization_config=None
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    bleu_scores = {}
    os.makedirs(model_id, exist_ok=True)

    for pair_id, langs in PAIR_LANGUAGES.items():
        src_lang, tgt_lang = langs
        input_file = f"flores200.{src_lang[:3].lower()}"
        reference_file = f"flores200.{tgt_lang[:3].lower()}"
        hyp_file = f"{model_id}/{pair_id}.out"

        print(f"\n[{model_id}] Translating {pair_id} ...")

        LINES = 1012
        if file_len(hyp_file) != LINES:
            with open(input_file, "r") as src, open(hyp_file, "w") as out:
                count = 0
                for line in src:
                    translated = llm_translate(model, tokenizer, line.strip(), src_lang, tgt_lang)
                    print(f"{line.strip()} - {translated}")
                    out.write(translated + "\n")
                    count += 1
                    if count % 50 == 0:
                        print(f"{count}/{LINES} lines translated...")

        # Compute BLEU
        bleu = get_sacrebleu(reference_file, hyp_file)
        bleu_scores[pair_id] = bleu
        print(f"BLEU {pair_id}: {bleu}")

    end_time = datetime.datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    bleu_scores["evaluation_time_seconds"] = elapsed

    save_model_bleu(model_id, bleu_scores)
    return model_id, elapsed

# ----------------------------------------------------------
# Master loop: evaluate all models in MODELS array
# ----------------------------------------------------------
def main():
    total_start = datetime.datetime.now()
    timing_info = {}

    for model_path in MODELS:
        model_name, elapsed = evaluate_model(model_path)
        timing_info[model_name] = elapsed

    # Save timing info to JSON
    with open("model_times.json", "w") as f:
        json.dump(timing_info, f, indent=4)
    print("\nAll models evaluated.")
    print("Total time:", datetime.datetime.now() - total_start)
    print("Timing info saved to model_times.json")

if __name__ == "__main__":
    main()

