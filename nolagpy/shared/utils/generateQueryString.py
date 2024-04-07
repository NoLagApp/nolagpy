from typing import Dict


def generateQueryString(query: Dict[str, any]) -> str:
    query_array = []
    for key, value in query.items():
        query_array.append(f"{key}={value}")
    query_string = "&".join(query_array)
    return f"?{query_string}" if query_string else ""
