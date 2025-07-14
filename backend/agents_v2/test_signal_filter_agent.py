# test_signal_filter_agent.py

import asyncio
from backend.agents_v2.signal_filter import SignalFilterAgent, URLInfo

async def main():
    urls = [
        URLInfo(
            url="https://techcrunch.com/2024/07/10/top-ai-startups-2024/",
            title="Top AI Startups to Watch in 2024",
            snippet="TechCrunch compiles a list of the most promising AI companies..."
        ),
        URLInfo(
            url="https://medium.com/some-random-thoughts-about-life",
            title="Why I Quit My Job to Travel",
            snippet="This personal story has nothing to do with business partnerships."
        ),
        URLInfo(
            url="https://www.gartner.com/en/articles/how-to-choose-your-next-data-platform",
            title="How to Choose Your Next Data Platform",
            snippet="This article outlines technical factors but does not list companies."
        ),
        URLInfo(
            url="https://dealroom.co/industries/biotech",
            title="Top Biotech Startups in Europe",
            snippet="Dealroom's curated list of biotech innovators and disruptors."
        )
    ]

    agent = SignalFilterAgent()
    filtered = await agent.filter(urls)

    print(filtered)

if __name__ == "__main__":
    asyncio.run(main())
