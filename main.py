import argparse

from dcinside import Crawler
from dcinside.exception import ServerException, DeletedPostException, StaleElementException
parser = argparse.ArgumentParser(description="DCInside 크롤러")

parser.add_argument("--gallery", required=True, help="Name of gallery (ex: leagueoflegends3)")
parser.add_argument("--start_idx", type=int, default=1, help="Start index of gallery page")
parser.add_argument("--end_idx", type=int, required=True, help="End index of gallery page")
parser.add_argument("--chrome_driver", required=True, help="Path to chrome driver")

args = parser.parse_args()

crawler = Crawler(args.chrome_driver, timeout=60, retry=True)

for page_idx in range(args.start_idx, args.end_idx + 1):
    try:
        post = crawler.crawl(args.gallery, page_idx)
        print(f"\n=== Post #{page_idx} ===")
        print(f"Title: {post['title']}")
        print(f"Content:\n{post['content']}\n")

        print("--- Comments ---")
        for idx, comment in enumerate(post["comments"], 1):
            if isinstance(comment, dict):
                print(f"{idx}. {comment.get('content', '')}")
            else:
                print(f"{idx}. {comment}")
        print("=" * 30)

    except (ServerException, DeletedPostException) as e:
        print(f"Error on page {page_idx}: {e}")
