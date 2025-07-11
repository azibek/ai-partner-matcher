import asyncio
from util_gsearch import fetch_duckduckgo_results

async def main():
    query = "Innovation consultancy firm canada"
    results = await fetch_duckduckgo_results(query, num=10)

    print("\n--- DuckDuckGo Search Results ---")
    for i, link in enumerate(results, start=1):
        print(f"{i}. {link}")

if __name__ == "__main__":
    asyncio.run(main())
