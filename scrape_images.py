# E-Waste Image Scraper - Modern Implementation
# Scrapes images using DuckDuckGo (no API key needed)

from duckduckgo_search import DDGS
import requests
from pathlib import Path
from urllib.parse import urlparse
import time
from typing import List, Dict
import hashlib


# Define e-waste categories with specific search terms
CATEGORIES = {
    'mobile_phones': [
        'broken mobile phone e-waste',
        'old smartphones recycling',
        'discarded cell phones',
        'mobile phone waste pile'
    ],
    'laptops': [
        'old laptop e-waste',
        'broken laptop recycling',
        'discarded computers',
        'laptop electronic waste'
    ],
    'monitors': [
        'old computer monitor waste',
        'broken screen e-waste',
        'discarded monitors',
        'CRT monitor waste'
    ],
    'cables_wires': [
        'electronic cables waste',
        'wire e-waste pile',
        'discarded cables',
        'electronic wire scrap'
    ],
    'circuit_boards': [
        'circuit board e-waste',
        'PCB electronic waste',
        'computer motherboard scrap',
        'electronic circuit board recycling'
    ]
}


def download_image(url: str, save_path: Path, timeout: int = 10) -> bool:
    """
    Download a single image from URL
    
    Args:
        url: Image URL
        save_path: Path to save the image
        timeout: Request timeout in seconds
        
    Returns:
        True if successful, False otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()
        
        # Check if it's an image
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type.lower():
            return False
        
        # Save image
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Verify file was created and has content
        if save_path.exists() and save_path.stat().st_size > 0:
            return True
        else:
            save_path.unlink(missing_ok=True)
            return False
            
    except Exception as e:
        print(f"Failed to download: {str(e)[:50]}")
        return False


def scrape_category(category_name: str, search_queries: List[str], 
                   images_per_query: int = 50) -> int:
    """
    Scrape images for a specific e-waste category
    
    Args:
        category_name: Name of the category folder
        search_queries: List of search terms
        images_per_query: Number of images to download per query
        
    Returns:
        Total number of images downloaded
    """
    print(f"\n{'='*60}")
    print(f"Category: {category_name.upper().replace('_', ' ')}")
    print(f"{'='*60}")
    
    # Create output directory
    output_dir = Path(f"data/raw/{category_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    total_downloaded = 0
    
    for query_idx, query in enumerate(search_queries, 1):
        print(f"\n[{query_idx}/{len(search_queries)}] Searching: '{query}'")
        
        try:
            # Search for images using DuckDuckGo
            with DDGS() as ddgs:
                results = ddgs.images(
                    keywords=query,
                    max_results=images_per_query,
                    safesearch='off'
                )
                
                downloaded = 0
                for idx, result in enumerate(results, 1):
                    try:
                        # Create unique filename using hash of URL
                        url_hash = hashlib.md5(result['image'].encode()).hexdigest()[:12]
                        ext = Path(urlparse(result['image']).path).suffix or '.jpg'
                        filename = f"{category_name}_{query_idx}_{url_hash}{ext}"
                        save_path = output_dir / filename
                        
                        # Skip if already exists
                        if save_path.exists():
                            continue
                        
                        # Download image
                        if download_image(result['image'], save_path):
                            downloaded += 1
                            print(f"   ✓ Downloaded {downloaded}/{images_per_query}: {filename}")
                        
                        # Small delay to be respectful
                        time.sleep(0.1)
                        
                    except Exception as e:
                        print(f"   ✗ Error with image {idx}: {str(e)[:50]}")
                        continue
                
                total_downloaded += downloaded
                print(f"   → Downloaded {downloaded} images for this query")
                
                # Delay between queries
                time.sleep(1)
                
        except Exception as e:
            print(f"   ✗ Error with query '{query}': {str(e)}")
            continue
    
    print(f"\nTotal images downloaded for {category_name}: {total_downloaded}")
    return total_downloaded


def scrape_all_categories():
    """
    Scrape images for all e-waste categories
    """
    print("\n" + "="*60)
    print("E-WASTE IMAGE SCRAPER")
    print("="*60)
    print(f"\nCategories to scrape: {len(CATEGORIES)}")
    print(f"Target images per category: ~200")
    print(f"Estimated time: 10-15 minutes")
    print("\n" + "="*60)
    
    # Create data directory
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    
    # Track results
    results = {}
    
    # Scrape each category
    for category, queries in CATEGORIES.items():
        count = scrape_category(category, queries, images_per_query=50)
        results[category] = count
    
    # Final summary
    print("\n" + "="*60)
    print("SCRAPING COMPLETE!")
    print("="*60)
    print("\nSummary:")
    print("-" * 60)
    
    total_images = 0
    for category, count in results.items():
        total_images += count
        print(f"   {category.ljust(20)}: {count:>4} images")
    
    print("-" * 60)
    print(f"   {'TOTAL'.ljust(20)}: {total_images:>4} images")
    print("="*60)
    
    print("\nImages saved to: data/raw/")
    print("Ready for preprocessing and training!\n")


if __name__ == "__main__":
    scrape_all_categories()