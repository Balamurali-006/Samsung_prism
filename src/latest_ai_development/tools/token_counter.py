import tiktoken
import json

# Global token tracking per LLM
token_usage = {
    "input_tokens": 0,
    "output_tokens": 0,
    "total_tokens": 0,
    "by_model": {}
}

def count_tokens(text: str) -> int:
    """Count tokens in text using cl100k_base encoding."""
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def track_token_usage(model_name: str, input_count: int, output_count: int):
    """Track token usage for a specific model."""
    total = input_count + output_count
    
    # Update global counters
    token_usage["input_tokens"] += input_count
    token_usage["output_tokens"] += output_count
    token_usage["total_tokens"] += total
    
    # Track by model
    if model_name not in token_usage["by_model"]:
        token_usage["by_model"][model_name] = {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "calls": 0
        }
    
    token_usage["by_model"][model_name]["input_tokens"] += input_count
    token_usage["by_model"][model_name]["output_tokens"] += output_count
    token_usage["by_model"][model_name]["total_tokens"] += total
    token_usage["by_model"][model_name]["calls"] += 1
    
    # Print token usage for this call
    print(f"\n📊 Token Usage - {model_name}:")
    print(f"   Input: {input_count:,} tokens")
    print(f"   Output: {output_count:,} tokens")
    print(f"   Total: {total:,} tokens")


def estimate_tokens_for_model(text: str, model_name: str) -> int:
    """Estimate tokens for a specific model using appropriate encoding."""
    try:
        if "gpt" in model_name.lower():
            enc = tiktoken.get_encoding("cl100k_base")  # For GPT-3.5/GPT-4
        elif "claude" in model_name.lower():
            enc = tiktoken.get_encoding("cl100k_base")  # Claude uses similar tokenization
        else:
            # Default for Groq and other models
            enc = tiktoken.get_encoding("cl100k_base")
        
        return len(enc.encode(text))
    except Exception as e:
        print(f"⚠️ Error estimating tokens: {e}")
        return 0


def get_token_summary() -> str:
    """Get a summary of all token usage."""
    summary = "\n" + "="*60
    summary += "\n📈 TOTAL TOKEN USAGE SUMMARY"
    summary += "\n" + "="*60
    summary += f"\nGlobal Input Tokens: {token_usage['input_tokens']:,}"
    summary += f"\nGlobal Output Tokens: {token_usage['output_tokens']:,}"
    summary += f"\nGlobal Total Tokens: {token_usage['total_tokens']:,}"
    summary += "\n\n📊 Breakdown by Model:"
    summary += "\n" + "-"*60
    
    for model_name, stats in token_usage["by_model"].items():
        summary += f"\n{model_name}:"
        summary += f"\n  Calls: {stats['calls']}"
        summary += f"\n  Input: {stats['input_tokens']:,} tokens"
        summary += f"\n  Output: {stats['output_tokens']:,} tokens"
        summary += f"\n  Total: {stats['total_tokens']:,} tokens"
        if stats['calls'] > 0:
            avg_tokens = stats['total_tokens'] // stats['calls']
            summary += f"\n  Avg per call: {avg_tokens:,} tokens"
        summary += "\n"
    
    summary += "="*60 + "\n"
    return summary


def reset_token_tracking():
    """Reset token tracking counters."""
    global token_usage
    token_usage = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "by_model": {}
    }
