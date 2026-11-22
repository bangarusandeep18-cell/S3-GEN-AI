import csv
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "openai-community/gpt2"
PROMPTS = ["The cat is", "Artificial intelligence is", "India is a", "Machine learning helps"]
TOP_K = 5
OUTPUT_FILE = Path(__file__).with_name("week7_probability_results.csv")


def main():
    print(f"Loading {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.eval()
    results=[]
    for prompt in PROMPTS:
        inputs=tokenizer(prompt,return_tensors="pt")
        with torch.inference_mode(): outputs=model(**inputs)
        probabilities=torch.softmax(outputs.logits[0,-1,:],dim=-1)
        top_probs,top_ids=torch.topk(probabilities,TOP_K)
        print("\n"+"="*60+f"\nPROMPT: {prompt}\nInput Token IDs: {inputs['input_ids'][0].tolist()}")
        for rank,(token_id,probability) in enumerate(zip(top_ids,top_probs),1):
            token=tokenizer.decode([token_id.item()]); prob=probability.item()
            print(f"Rank: {rank} | Token: {token!r} | Probability: {prob:.6f}")
            results.append([prompt,rank,token,token_id.item(),round(prob,6)])
    with OUTPUT_FILE.open("w",newline="",encoding="utf-8-sig") as file:
        writer=csv.writer(file); writer.writerow(["Prompt","Rank","Candidate Token","Token ID","Probability"]); writer.writerows(results)
    print(f"\nResults saved to {OUTPUT_FILE.name}")


if __name__ == "__main__": main()
