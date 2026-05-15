from const import (
    INPUT_PRICE_PER_1M,
    CACHED_INPUT_PRICE_PER_1M,
    OUTPUT_PRICE_PER_1M
)

from schemas import UsageResponse


def calculate_cost(usage):

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens

    cached_tokens = 0

    if hasattr(usage, "prompt_tokens_details"):

        details = usage.prompt_tokens_details

        if details and hasattr(details, "cached_tokens"):
            cached_tokens = details.cached_tokens

    non_cached_prompt_tokens = prompt_tokens - cached_tokens

    input_cost = (
        non_cached_prompt_tokens / 1_000_000
    ) * INPUT_PRICE_PER_1M

    cached_cost = (
        cached_tokens / 1_000_000
    ) * CACHED_INPUT_PRICE_PER_1M

    output_cost = (
        completion_tokens / 1_000_000
    ) * OUTPUT_PRICE_PER_1M

    total_cost = input_cost + cached_cost + output_cost

    return UsageResponse(
        prompt_tokens=prompt_tokens,
        cached_tokens=cached_tokens,
        completion_tokens=completion_tokens,
        input_cost=input_cost,
        cached_cost=cached_cost,
        output_cost=output_cost,
        total_cost=total_cost
    )