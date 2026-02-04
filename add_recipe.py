#!/usr/bin/env python3
"""
🥗 RECIPE EXTRACTOR & ADDER
When Zain sends a Facebook recipe link, I extract and add it to the vault
"""

import json
import requests
from datetime import datetime

API_URL = "http://localhost:8000/api/recipes"  # Will update when deployed

def extract_recipe_from_facebook(url):
    """
    Extract recipe details from Facebook video/post
    For now, using placeholder - will integrate with scraping
    """
    
    # TODO: Integrate with Facebook scraping or manual input
    # For now, return template for manual filling
    
    return {
        'name': '',  # To be filled
        'category': '',  # breakfast/lunch/dinner/dessert/snack
        'cuisine': '',  # italian/mexican/indian/asian/etc
        'calories': 0,
        'cookTime': '',
        'ingredients': [],
        'method': [],
        'fb_url': url,
        'added_by': 'Blaze',
        'date_added': datetime.now().strftime('%Y-%m-%d')
    }

def add_recipe_to_vault(recipe_data):
    """Add recipe to backend database"""
    try:
        response = requests.post(API_URL, json=recipe_data)
        if response.status_code == 201:
            print(f"✅ Recipe added: {recipe_data['name']}")
            return response.json()
        else:
            print(f"❌ Failed to add: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def process_facebook_link(fb_url):
    """
    Main function: Extract recipe from Facebook and add to vault
    
    Usage:
        python3 add_recipe.py "https://facebook.com/share/r/ABC123"
    """
    print(f"🔍 Processing Facebook link: {fb_url}")
    print()
    
    # Step 1: Extract recipe data
    recipe = extract_recipe_from_facebook(fb_url)
    
    print("📋 EXTRACTED RECIPE DATA:")
    print(f"   Facebook URL: {fb_url}")
    print()
    
    # For now, display template for manual verification
    print("📝 RECIPE TEMPLATE (Fill in the details):")
    print(json.dumps(recipe, indent=2))
    print()
    
    print("⚠️  NOTE: Full automation requires:")
    print("   1. Backend server deployment")
    print("   2. Facebook scraping integration")
    print("   3. Updated Recipe Vault frontend")
    print()
    
    print("📱 TO ADD RECIPE MANUALLY:")
    print("   1. Extract ingredients and steps from Facebook")
    print("   2. Update this script with recipe details")
    print("   3. Run: python3 add_recipe.py")
    print()
    
    return recipe

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        fb_url = sys.argv[1]
        process_facebook_link(fb_url)
    else:
        print("Usage: python3 add_recipe.py <facebook_url>")
        print("Example: python3 add_recipe.py 'https://facebook.com/share/r/ABC123'")
