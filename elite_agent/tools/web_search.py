"""Web search tool using the Tavily API."""

from langchain_core.tools import tool

from ..config.settings import settings


@tool
def web_search_tool(query: str) -> str:
    """Search the internet for up-to-date information using Tavily.

    Args:
        query: The search query string.

    Returns:
        A formatted string containing a direct answer (if available) and
        the top search results with titles, URLs and content snippets.
    """
    try:
        from tavily import TavilyClient  # type: ignore[import-untyped]

        client = TavilyClient(api_key=settings.tavily_api_key)
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
        )

        parts: list[str] = []

        answer = response.get("answer", "")
        if answer:
            parts.append(f"**Qisqa javob:** {answer}\n")

        results = response.get("results", [])
        if results:
            parts.append("**Batafsil natijalar:**")
            for i, result in enumerate(results, start=1):
                title = result.get("title", "Sarlavha yo'q")
                url = result.get("url", "")
                content = result.get("content", "")[:500]
                parts.append(f"{i}. **{title}**\n   URL: {url}\n   {content}")

        return "\n\n".join(parts) if parts else "Natija topilmadi."

    except Exception as exc:  # noqa: BLE001
        return f"Qidiruv xatosi: {exc}"
