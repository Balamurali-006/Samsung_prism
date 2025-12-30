"""
LLM wrapper to track token usage across API calls.
"""
from crewai import LLM
from tools.token_counter import track_token_usage, estimate_tokens_for_model


class TokenTrackingLLM(LLM):
    """Wrapper around LLM that tracks token usage."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_model = self.model if hasattr(self, 'model') else 'unknown'
    
    def call(self, messages, *args, **kwargs):
        """Override call method to track tokens."""
        # Estimate input tokens
        input_text = ""
        for msg in messages:
            if isinstance(msg, dict) and "content" in msg:
                input_text += msg["content"] + " "
            else:
                input_text += str(msg) + " "
        
        input_tokens = estimate_tokens_for_model(input_text, self._original_model)
        
        # Make the actual call
        response = super().call(messages, *args, **kwargs)
        
        # Estimate output tokens (from response)
        if response:
            output_text = str(response) if not isinstance(response, str) else response
            output_tokens = estimate_tokens_for_model(output_text, self._original_model)
        else:
            output_tokens = 0
        
        # Track the usage
        track_token_usage(self._original_model, input_tokens, output_tokens)
        
        return response
