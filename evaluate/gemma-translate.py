#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import datetime
import torch
from transformers import pipeline

print("PyTorch threads:", torch.get_num_threads())

# ----------------------------------------------------------
# CONFIG: List of models to evaluate
# ----------------------------------------------------------
MODELS = [
#    "google/translategemma-27b-it",
    "google/translategemma-4b-it",
    # Add more models here:
    # "google/translategemma-2b-it",
]

# ----------------------------------------------------------
# FLORES LANG PAIRS
# Language codes for TranslateGemma
# See: https://huggingface.co/google/translategemma-4b-it for supported codes
# ----------------------------------------------------------
PAIR_LANGUAGES = {
    "en-ca": {
        "src_code": "en",
        "tgt_code": "ca",
        "src_name": "English",
        "tgt_name": "Catalan",
    },
    # Add more language pairs as needed:
    # "en-es": {
    #     "src_code": "en",
    #     "tgt_code": "es",
    #     "src_name": "English",
    #     "tgt_name": "Spanish",
    # },
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


def llm_translate(pipe, text, src_lang_code, tgt_lang_code):
    """
    Translate text using TranslateGemma pipeline.
    
    Args:
        pipe: The transformers pipeline
        text: Text to translate
        src_lang_code: Source language code (e.g., "en")
        tgt_lang_code: Target language code (e.g., "ca")
    
    Returns:
        Translated text string
    """
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "source_lang_code": src_lang_code,
                    "target_lang_code": tgt_lang_code,
                    "text": text,
                }
            ],
        }
    ]
    
    output = pipe(text=messages)
    
    # Extract the generated translation from the output
    translated = output[0]["generated_text"][-1]["content"]
    
    # Clean up the output (remove any extra whitespace/newlines)
    return translated.strip()


# ----------------------------------------------------------
# Evaluation loop for one model
# ----------------------------------------------------------
def evaluate_model(model_path):
    model_id = model_path.split("/")[-1]

    start_time = datetime.datetime.now()
    print("=" * 80)
    print(f"Evaluating model: {model_id}  ({model_path})")
    print("=" * 80)

    # Initialize the pipeline
    # Use "cuda" if GPU available, otherwise "cpu"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    device = "cpu"
    print(f"Using device: {device}")
    
    pipe = pipeline(
        "image-text-to-text",
        model=model_path,
        device=device,
        torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32,
    )

    bleu_scores = {}
    os.makedirs(model_id, exist_ok=True)

    for pair_id, lang_info in PAIR_LANGUAGES.items():
        src_code = lang_info["src_code"]
        tgt_code = lang_info["tgt_code"]
        src_name = lang_info["src_name"]
        tgt_name = lang_info["tgt_name"]
        
        input_file = f"flores200.{src_name[:3].lower()}"
        reference_file = f"flores200.{tgt_name[:3].lower()}"
        hyp_file = f"{model_id}/{pair_id}.out"

        print(f"\n[{model_id}] Translating {pair_id} ({src_name} -> {tgt_name})...")

        LINES = 1012
        if file_len(hyp_file) != LINES:
            with open(input_file, "r") as src, open(hyp_file, "w") as out:
                count = 0
                for line in src:
                    translated = llm_translate(
                        pipe, line.strip(), src_code, tgt_code
                    )
                    print(f"{count} - {line.strip()} - {translated}")
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
    
    # Free memory
    del pipe
    torch.cuda.empty_cache() if torch.cuda.is_available() else None
    
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
    
    print("\n" + "=" * 80)
    print("All models evaluated.")
    print("=" * 80)
    print("Total time:", datetime.datetime.now() - total_start)
    print("Timing info saved to model_times.json")
    
    # Print summary
    print("\nSummary:")
    for model_name, elapsed in timing_info.items():
        print(f"  {model_name}: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
