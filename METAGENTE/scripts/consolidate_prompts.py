import os
import json
import argparse
from string import Template
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prepare_sample import load_sample
from rouge_eval import calculate_rouge

try:
    from mistralai import Mistral
except ImportError:
    try:
        from mistralai.client.sdk import Mistral
    except ImportError:
        Mistral = None

mistral_client = None
resolved_model_name = None
quota_fallback_triggered = False

def init_mistral(requested_model: str):
    global mistral_client
    global resolved_model_name
    
    if not os.environ.get("MISTRAL_API_KEY"):
        print("Error: MISTRAL_API_KEY environment variable is not set.")
        sys.exit(1)
    if Mistral is None:
        print("Error: mistralai package is not installed. Please run: pip install -r requirements.txt")
        sys.exit(1)
        
    try:
        mistral_client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))
    except Exception as e:
        print(f"Error initializing Mistral client: {e}")
        sys.exit(1)
        
    resolved_model_name = requested_model

#funciones de llamada a llm

def run_extractor(prompt_template: str, readme_text: str, mode: str = "mock") -> str:
    """Extractor Call (Mock or Mistral with Quota Fallback)"""
    global quota_fallback_triggered
    prompt = Template(prompt_template).substitute(readme_text=readme_text)
    
    if mode == "mistral":
        try:
            response = mistral_client.chat.complete(
                model=resolved_model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "limit" in error_str.lower():
                print("\n[Warning] Live API call failed due to provider quota/billing limits (429).")
                print("-> Falling back to mock execution for Extractor.")
                quota_fallback_triggered = True
            else:
                print(f"\n[Warning] Unexpected API Error: {error_str}\n-> Falling back to mock execution.")
                quota_fallback_triggered = True

    return "MOCK EXTRACTED TEXT: FastLogger is a fast logging library."

def run_summarizer(prompt_template: str, extracted_text: str, mode: str = "mock") -> str:
    """Summarizer Call (Mock or Mistral with Quota Fallback)"""
    global quota_fallback_triggered
    prompt = Template(prompt_template).substitute(extracted_text=extracted_text)
    
    if mode == "mistral":
        try:
            response = mistral_client.chat.complete(
                model=resolved_model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "limit" in error_str.lower():
                print("\n[Warning] Live API call failed due to provider quota/billing limits (429).")
                print("-> Falling back to mock execution for Summarizer.")
                quota_fallback_triggered = True
            else:
                print(f"\n[Warning] Unexpected API Error: {error_str}\n-> Falling back to mock execution.")
                quota_fallback_triggered = True

    return "FastLogger is a fast logging library."

def run_teacher(prompt_template: str, extracted_text: str, description: str, 
                generated_about: str, rouge_score: float, summarizer_prompt: str, mode: str = "mock") -> str:
    """Teacher Call (Currently always Mocked as per requirements)"""
    prompt = Template(prompt_template).substitute(
        extracted_text=extracted_text,
        description=description,
        generated_about=generated_about,
        rouge_score=rouge_score,
        summarizer_prompt=summarizer_prompt
    )
    return "MOCK TEACHER FEEDBACK: Focus more on zero-dependency. Prompt: Summarize carefully."

def run_prompt_creator(prompt_template: str, summarizer_list: str, mode: str = "mock") -> str:
    """Prompt Creator Call (Currently always Mocked as per requirements)"""
    prompt = Template(prompt_template).substitute(summarizer_list=summarizer_list)
    return "MOCK FINAL PROMPT: Summarize the following extracted text, emphasizing that it is zero-dependency."

#flujo de orquestación principal

def main():
    parser = argparse.ArgumentParser(description="Run the Metagente optimization cycle.")
    parser.add_argument("--mode", type=str, choices=["mock", "mistral"], default="mock", help="Execution mode")
    parser.add_argument("--model", type=str, default="mistral-large-latest", help="Requested model name for API calls")
    parser.add_argument("--epochs", type=int, default=3, help="Number of optimization epochs")
    args = parser.parse_args()

    print("="*50)
    if args.mode == "mistral":
        init_mistral(args.model)
        print(f"Executing in MISTRAL Mode")
        print(f"Active Model: {resolved_model_name}")
    else:
        print("Executing in MOCK Mode")
        print("All LLM inferences will be simulated deterministically.")
    print("="*50)

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_train_dir = os.path.join(project_root, "data", "train")
    
#cargamos los ejemplos, habilitado para batch optimization
    samples_data = []
    try:
        for filename in os.listdir(data_train_dir):
            if filename.endswith(".txt"):
                sample_name = filename[:-4]
                samples_data.append(load_sample(sample_name, base_dir=os.path.join(project_root, "data")))
    except FileNotFoundError as e:
        print(f"Error loading samples: {e}")
        return

    if not samples_data:
        print("No samples found in data/train.")
        return

#cargamos los prompts de los 4 agentes
    prompts_dir = os.path.join(project_root, "prompts")
    with open(os.path.join(prompts_dir, "extractor.md"), "r", encoding="utf-8") as f:
        extractor_prompt = f.read()
    with open(os.path.join(prompts_dir, "summarizer_initial.md"), "r", encoding="utf-8") as f:
        summarizer_prompt = f.read()
    with open(os.path.join(prompts_dir, "teacher.md"), "r", encoding="utf-8") as f:
        teacher_prompt = f.read()
    with open(os.path.join(prompts_dir, "prompt_creator.md"), "r", encoding="utf-8") as f:
        creator_prompt = f.read()

    print(f"\nStarting Batch Optimization cycle for {len(samples_data)} samples.\n")

    runs_dir = os.path.join(project_root, "runs")
    mode_suffix = f"_{args.mode}"

#batch extraction
    print("-> Running Extractor (One-time) for all samples...")
    extracted_texts = {}
    for sample in samples_data:
        extracted_text = run_extractor(extractor_prompt, sample["train_content"], mode=args.mode)
        extracted_texts[sample["sample_name"]] = extracted_text
        with open(os.path.join(runs_dir, "logs", f"extracted_text_{sample['sample_name']}{mode_suffix}.txt"), "w", encoding="utf-8") as f:
            f.write(extracted_text)
        
    current_summarizer_prompt = summarizer_prompt
    
#ciclo de épocas
    for epoch in range(1, args.epochs + 1):
        print(f"\n--- EPOCH {epoch}/{args.epochs} ---")
        
        batch_teacher_feedback = ""
        total_rougeL = 0.0
        
        for sample in samples_data:
            sample_name = sample["sample_name"]
            
            print(f"   -> Processing {sample_name}...")
            generated_summary = run_summarizer(current_summarizer_prompt, extracted_texts[sample_name], mode=args.mode)
            
            scores = calculate_rouge(sample["ref_content"], generated_summary)
            total_rougeL += scores['rougeL']
            
            teacher_feedback = run_teacher(
                prompt_template=teacher_prompt,
                extracted_text=extracted_texts[sample_name],
                description=sample["ref_content"],
                generated_about=generated_summary,
                rouge_score=scores["rougeL"],
                summarizer_prompt=current_summarizer_prompt,
                mode=args.mode
            )
            
            batch_teacher_feedback += f"\n--- Feedback for {sample_name} ---\n{teacher_feedback}\n"
            
            epoch_suffix = f"{mode_suffix}_epoch{epoch}"
            with open(os.path.join(runs_dir, "candidates", f"candidate_{sample_name}{epoch_suffix}.txt"), "w", encoding="utf-8") as f:
                f.write(generated_summary)
            with open(os.path.join(runs_dir, "metrics", f"metrics_{sample_name}{epoch_suffix}.json"), "w", encoding="utf-8") as f:
                json.dump(scores, f, indent=4)
            with open(os.path.join(runs_dir, "logs", f"teacher_feedback_{sample_name}{epoch_suffix}.txt"), "w", encoding="utf-8") as f:
                f.write(teacher_feedback)

        avg_rougeL = total_rougeL / len(samples_data)
        print(f"-> Batch Average ROUGE-L: {avg_rougeL:.4f}")

        print("-> Running Prompt Creator on batch feedback...")
        final_prompt = run_prompt_creator(creator_prompt, summarizer_list=batch_teacher_feedback, mode=args.mode)
        
#actualizamos el prompt summarizer
        current_summarizer_prompt = final_prompt
        
        with open(os.path.join(runs_dir, "summaries", f"optimized_prompt_batch{mode_suffix}_epoch{epoch}.md"), "w", encoding="utf-8") as f:
            f.write(final_prompt)

    if quota_fallback_triggered:
        note_content = (
            f"NOTE: The script was executed in '{args.mode}' mode, but due to provider quota "
            "or billing limits (e.g., 429), the live API calls failed. "
            "The system gracefully degraded and used mock outputs to successfully complete the pipeline."
        )
        with open(os.path.join(runs_dir, "logs", f"quota_fallback_note{mode_suffix}.txt"), "w", encoding="utf-8") as f:
            f.write(note_content)

    print("\nBatch Optimization cycle complete. Artifacts saved to runs/.")

if __name__ == "__main__":
    main()
