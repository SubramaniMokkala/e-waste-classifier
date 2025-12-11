# E-Waste Image Scraper
# Scrapes images from Bing for different e-waste categories

from bing_image_downloader import downloader
import os


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


def scrape_category(category_name, search_queries, images_per_query=50):
    """
    Scrape images for a specific e-waste category
    
    Args:
        category_name: Name of the category folder
        search_queries: List of search terms
        images_per_query: Number of images to download per query
    """
    print(f"\n{'-'*60}")
    print(f"Scraping category: {category_name}")
    print(f"{'-'*60}")
    
    output_dir = f"data/raw/{category_name}"
    
    for query in search_queries:
        print(f"\nSearching: '{query}'")
        
        try:
            downloader.download(
                query=query,
                limit=images_per_query,
                output_dir=output_dir,
                adult_filter_off=True,
                force_replace=False,
                timeout=60,
                verbose=True
            )
            print(f"Downloaded images for: {query}")
            
        except Exception as e:
            print(f"Error with query '{query}': {str(e)}")
            continue
    
    # Count total images
    try:
        category_path = os.path.join(output_dir, list(search_queries)[0].replace(' ', '_'))
        if os.path.exists(category_path):
            num_images = len([f for f in os.listdir(category_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
            print(f"\nTotal images for {category_name}: {num_images}")
    except:
        pass


def scrape_all_categories():
    """
    Scrape images for all e-waste categories
    """
    print("\n" + "-"*60)
    print("E-WASTE IMAGE SCRAPER")
    print("-"*60)
    print(f"\nCategories to scrape: {len(CATEGORIES)}")
    print(f"Target images per category: ~200")
    print("\nThis will take 10-15 minutes...")
    print("-"*60)
    
    # Create data directory
    os.makedirs("data/raw", exist_ok=True)
    
    # Scrape each category
    for category, queries in CATEGORIES.items():
        scrape_category(category, queries, images_per_query=50)
    
    print("\n" + "-"*60)
    print("SCRAPING COMPLETE!")
    print("-"*60)
    
    # Summary
    print("\nSummary:")
    for category in CATEGORIES.keys():
        category_path = f"data/raw/{category}"
        if os.path.exists(category_path):
            # Count images in all subdirectories
            total_images = 0
            for root, dirs, files in os.walk(category_path):
                total_images += len([f for f in files if f.endswith(('.jpg', '.jpeg', '.png'))])
            print(f"   {category}: {total_images} images")



if __name__ == "__main__":
    # Run the scraper
    scrape_all_categories()