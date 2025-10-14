"""
Image Generation Service for Esoteric Themes
Генерация изображений для астрологии, нумерологии, матрицы судьбы, Human Design
"""

import os
import requests
from pathlib import Path
from urllib.parse import quote
from datetime import datetime
from typing import Optional

class ImageGenerator:
    """Generate esoteric-themed images using Pollinations.ai (FREE!)"""
    
    # Esoteric theme prompts
    THEME_PROMPTS = {
        "astrology": "Mystical zodiac wheel with all 12 signs, cosmic background, stars, planets, ethereal glow, spiritual art, high quality, detailed",
        "numerology": "Sacred numerology symbols, golden numbers 1-9 in mystical circle, divine geometry, spiritual energy, cosmic background, high detail",
        "matrix": "Destiny matrix energy map, sacred geometry, chakra colors, spiritual pathways, mystical symbols, glowing mandala, cosmic energy",
        "human_design": "Human Design body graph, energy centers, spiritual diagram, colorful chakras, cosmic consciousness, mystical blueprint",
        "motivation": "Inspiring cosmic energy, spiritual awakening, golden light, universe connection, meditation vibes, peaceful atmosphere, ethereal beauty",
        "moon": "Mystical moon phases, intuitive wisdom, celestial magic, spiritual feminine energy, night sky, stars, ethereal glow",
        "tarot": "Mystical tarot cards spread, divine symbols, spiritual guidance, cosmic wisdom, ethereal art, magical atmosphere",
        "chakras": "Seven colorful chakras energy centers, spiritual alignment, cosmic healing, rainbow aura, divine light, meditation",
        "cosmic": "Deep space cosmos, nebula colors, spiritual universe, infinite energy, celestial beauty, mystical stars",
        "sacred_geometry": "Sacred geometry patterns, flower of life, metatron cube, divine proportions, golden ratio, spiritual symbols"
    }
    
    def __init__(self, storage_path: str = None):
        """Initialize image generator"""
        self.storage_path = Path(storage_path) if storage_path else Path("storage/backgrounds")
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def generate_background(
        self,
        theme: str = "cosmic",
        width: int = 1920,
        height: int = 1080,
        custom_prompt: str = None
    ) -> str:
        """
        Generate background image for video
        
        Args:
            theme: Theme name (astrology, numerology, matrix, etc.)
            width: Image width in pixels
            height: Image height in pixels  
            custom_prompt: Custom prompt (overrides theme)
            
        Returns:
            Path to saved image file
        """
        # Get prompt
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = self.THEME_PROMPTS.get(theme, self.THEME_PROMPTS["cosmic"])
        
        # Generate image URL
        encoded_prompt = quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
        
        try:
            # Download image
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            # Save to storage
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{theme}_{timestamp}.png"
            filepath = self.storage_path / filename
            
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            print(f"✅ Background generated: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating background: {e}")
            # Return default background if exists
            default = self.storage_path / "default_cosmic.png"
            if default.exists():
                return str(default)
            raise
    
    def generate_cover(
        self,
        theme: str,
        text_overlay: str = None,
        aspect_ratio: str = "16:9"
    ) -> str:
        """
        Generate video cover/thumbnail
        
        Args:
            theme: Theme name
            text_overlay: Optional text to overlay
            aspect_ratio: "16:9", "9:16" (vertical), "1:1" (square)
        
        Returns:
            Path to cover image
        """
        # Determine dimensions
        dimensions = {
            "16:9": (1920, 1080),
            "9:16": (1080, 1920),
            "1:1": (1080, 1080)
        }
        width, height = dimensions.get(aspect_ratio, (1920, 1080))
        
        # Get base prompt
        prompt = self.THEME_PROMPTS.get(theme, self.THEME_PROMPTS["cosmic"])
        
        # Add cover-specific styling
        prompt += ", professional cover art, eye-catching, vibrant colors, high quality"
        
        return self.generate_background(theme, width, height, prompt)
    
    def generate_for_script(self, script_text: str) -> str:
        """
        Auto-detect theme from script and generate matching background
        
        Args:
            script_text: Script content
            
        Returns:
            Path to generated background
        """
        script_lower = script_text.lower()
        
        # Theme detection
        if any(word in script_lower for word in ["зодиак", "знак", "гороскоп", "zodiac"]):
            theme = "astrology"
        elif any(word in script_lower for word in ["число", "нумерология", "number"]):
            theme = "numerology"
        elif any(word in script_lower for word in ["матрица", "карма", "matrix", "destiny"]):
            theme = "matrix"
        elif any(word in script_lower for word in ["дизайн", "тип", "human design", "генератор", "проектор"]):
            theme = "human_design"
        elif any(word in script_lower for word in ["луна", "moon", "интуиция"]):
            theme = "moon"
        elif any(word in script_lower for word in ["таро", "карты", "tarot"]):
            theme = "tarot"
        elif any(word in script_lower for word in ["чакра", "энергия", "chakra"]):
            theme = "chakras"
        else:
            theme = "cosmic"
        
        return self.generate_background(theme)
    
    def get_direct_url(
        self,
        theme: str = "cosmic",
        width: int = 1920,
        height: int = 1080
    ) -> str:
        """
        Get direct URL to generated image (without saving)
        
        Returns:
            Direct image URL
        """
        prompt = self.THEME_PROMPTS.get(theme, self.THEME_PROMPTS["cosmic"])
        encoded_prompt = quote(prompt)
        return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"


# Example usage
if __name__ == "__main__":
    generator = ImageGenerator()
    
    # Test all themes
    themes = ["astrology", "numerology", "matrix", "human_design", "motivation", "moon"]
    
    for theme in themes:
        print(f"\n🎨 Generating {theme}...")
        image_path = generator.generate_background(theme)
        print(f"✅ Saved: {image_path}")
    
    print("\n✨ All backgrounds generated!")

