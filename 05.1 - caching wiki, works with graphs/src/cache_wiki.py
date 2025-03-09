import argparse
import requests
from bs4 import BeautifulSoup
import json
import logging
from typing import Optional, Set, List, Dict, Tuple


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_wiki_page(title: str) -> Optional[str]:
    wiki_base_url: str = "https://en.wikipedia.org/wiki/"
    url: str = wiki_base_url + title.strip().replace(" ", "_")
    logging.info(f"Fetching: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"{e}")
        return None


def get_links(html_page: str) -> List[str]:
    soup = BeautifulSoup(html_page, "html.parser")
    seen: Set[str] = set()
    links: List[str] = []

    for link in soup.find_all("a", href=True):
        href: str = link["href"]
        if (
            href.startswith("/wiki/")
            and not href.endswith("/Main_Page")
            and not ":" in href
        ):
            title = href.split("/wiki/")[1]
            if title not in seen:
                links.append(title)
                seen.add(title)

    return links


def scan_wiki(
    start_page: str, depth: int, max_pages: int = 1000, min_pages: int = 20
) -> Dict[str, List[Dict[str, str]]]:
    nodes: List[Dict[str, str]] = []
    edges: List[Dict[str, str]] = []
    visited: Set[str] = set()
    to_visit: List[Tuple[str, int]] = [(start_page, 0)]
    links_count: int = 0

    while to_visit:
        current_page, current_depth = to_visit.pop(0)

        if current_page in visited or current_depth > depth:
            continue

        visited.add(current_page)
        page_html: str = get_wiki_page(current_page)

        if not page_html:
            continue

        links: Set[str] = get_links(page_html)
        nodes.append(current_page)

        if links_count > max_pages:
            logging.info("Page limit exceeded. Stopping scan")
            break

        for link in links:
            if link not in visited:
                links_count += 1
                if links_count > max_pages:
                    break
                edges.append({"source": current_page, "target": link})
                to_visit.append((link, current_depth + 1))

    if links_count < min_pages:
        logging.warning(
            f"Too few pages scanned: {page_count}. Choose another start page"
        )

    return {"nodes": [{"id": node} for node in nodes], "edges": edges}


def save_to_json(graph: Dict[str, List[str]], filename: str = "wiki.json") -> None:
    with open(filename, "w") as file:
        json.dump(graph, file, indent=4)
    logging.info(f"Graph saved to {filename}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan wiki pages and save links as graph."
    )
    parser.add_argument(
        "-p", "--page", type=str, default="Marketplace", help="Start wiki page"
    )
    parser.add_argument(
        "-d", "--depth", type=int, default=3, help="Links scanning depth"
    )

    args = parser.parse_args()

    graph = scan_wiki(args.page, args.depth)
    save_to_json(graph)


if __name__ == "__main__":
    main()
    print("Testing...")
    assert get_wiki_page("Erd%C5%91s_number") is not None, "Wiki page parsing error"
    html = """<table class="wikitable sortable">
<tbody><tr>
<th>Co-author</th>
<th>Number of <br />collaborations
</th></tr>
<tr>
<td><a href="/wiki/Andr%C3%A1s_S%C3%A1rk%C3%B6zy" title="András Sárközy">András Sárközy</a></td>
"""
    links = get_links(html)
    assert len(links) > 0, "Get links parser error"
    graph = scan_wiki(links[0], depth=1, max_pages=50)
    assert len(graph["nodes"]) > 0, "Nodes error"
    assert len(graph["edges"]) > 0, "Edges error"
    print("Test passed")
