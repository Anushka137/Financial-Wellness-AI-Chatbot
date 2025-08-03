import json
import os
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in {self.config_file}")
                return self.get_default_config()
        else:
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "GOOGLE_API_KEY": "",
            "API_KEY": "your-api-key",
            "API_URL": "http://localhost:8000"
        }
    
    def save_config(self):
        """Save current configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
    
    def validate_config(self) -> bool:
        """Validate that required configuration is present"""
        required_keys = ["GOOGLE_API_KEY", "API_URL"]
        missing_keys = [key for key in required_keys if not self.config.get(key)]
        
        if missing_keys:
            print(f"Missing required configuration: {', '.join(missing_keys)}")
            print("Please update your config.json file with the required values.")
            return False
        
        return True
    
    def setup_config(self):
        """Interactive setup for configuration"""
        print("Financial Wellness Chatbot Configuration Setup")
        print("=" * 50)
        
        # Google API Key
        google_key = input("Enter your Google Gemini API key (or press Enter to skip): ").strip()
        if google_key:
            self.set("GOOGLE_API_KEY", google_key)
        
        # API URL
        api_url = input("Enter API URL (default: http://localhost:8000): ").strip()
        if not api_url:
            api_url = "http://localhost:8000"
        self.set("API_URL", api_url)
        
        # API Key
        api_key = input("Enter API key (or press Enter for default): ").strip()
        if api_key:
            self.set("API_KEY", api_key)
        
        print("\nConfiguration saved!")
        print(f"Config file: {os.path.abspath(self.config_file)}")
        
        return self.validate_config()

if __name__ == "__main__":
    config = ConfigManager()
    if not config.validate_config():
        config.setup_config() 