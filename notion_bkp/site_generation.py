from pathlib import Path
import logging
import dateutil.parser as dt_parser
from urllib.parse import urljoin

def str_to_dt(structured_notion: dict):
    for page_id, page in structured_notion["pages"].items():
        for field in ['date', 'date_end', 'last_edited_time']:
            if field in page.keys():
                structured_notion["pages"][page_id][field] = dt_parser.isoparse(page[field])

def generate_page(page_id: str, structured_notion: dict, config: dict):
    page = structured_notion["pages"][page_id]
    page_url = page["url"]
    md_filename = page["title"] + '.md'

    folder = urljoin(page_url, '.')
    local_file_location = str(Path(folder).relative_to(Path(config["output_dir"]).resolve()))

    logging.debug(f"🤖 MD {Path(local_file_location) / md_filename}")

    (config["output_dir"] / Path(local_file_location)).mkdir(parents=True, exist_ok=True)
    
    md_file = (config["output_dir"] / Path(local_file_location) / md_filename).resolve()

    with open(md_file, 'w+', encoding='utf-8') as f:
        metadata = ("---\n"
                    f"title: {page['title']}\n"
                    f"cover: {page['cover']}\n"
                    f"icon: {page['icon']}\n"
                    f"emoji: {page['emoji']}\n")
        if "properties_md" in page.keys():
            for p_title, p_md in page["properties_md"].items():
                metadata += f"{p_title}: {p_md}\n"
        metadata += f"---\n\n"
        ### Complex part here
        md_content = page['md_content']
        md_content = metadata + md_content

        f.write(md_content)

def generate_pages(structured_notion: dict, config: dict):
    for page_id, page in structured_notion["pages"].items():
        generate_page(page_id, structured_notion, config)

def generate_site(structured_notion: dict, config: dict):
    generate_pages(structured_notion, config)
    logging.info("🤖 All md pages generated.")