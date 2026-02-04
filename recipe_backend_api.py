#!/usr/bin/env python3
"""
🥗 RECIPE BACKEND API
Central database for Recipe Vault - accessible from anywhere
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class RecipeDatabase:
    def __init__(self, db_file='recipes_database.json'):
        self.db_file = db_file
        self.recipes = self.load()
    
    def load(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return []
    
    def save(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.recipes, f, indent=2)
    
    def add_recipe(self, recipe_data):
        recipe = {
            'id': len(self.recipes) + 1,
            'date_added': datetime.now().isoformat(),
            **recipe_data
        }
        self.recipes.append(recipe)
        self.save()
        return recipe
    
    def get_all(self):
        return self.recipes
    
    def get_by_id(self, recipe_id):
        for r in self.recipes:
            if r['id'] == recipe_id:
                return r
        return None
    
    def update_recipe(self, recipe_id, data):
        for i, r in enumerate(self.recipes):
            if r['id'] == recipe_id:
                self.recipes[i].update(data)
                self.save()
                return self.recipes[i]
        return None

# Global database instance
db = RecipeDatabase()

class RecipeAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/recipes':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(db.get_all()).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/recipes':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            recipe_data = json.loads(post_data.decode())
            
            new_recipe = db.add_recipe(recipe_data)
            
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(new_recipe).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logs

def start_server(port=8000):
    server = HTTPServer(('0.0.0.0', port), RecipeAPIHandler)
    print(f"🥗 Recipe API Server running on port {port}")
    server.serve_forever()

if __name__ == '__main__':
    start_server()
