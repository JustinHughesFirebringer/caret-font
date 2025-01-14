import tkinter as tk
import math
from PIL import Image, ImageDraw, ImageTk

class FractalGlyphRenderer:
    def __init__(self, canvas):
        self.canvas = canvas
        
    def create_glyph_from_text(self, text):
        """Create an organic, flowing glyph based on input text"""
        self.canvas.delete('all')
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height / 2
        
        # Parse text into components
        words = text.split()
        main_text = ' '.join(words[:3]) if words else "Core"
        sub_texts = [' '.join(words[i:i+2]) for i in range(3, len(words), 2)]
        
        # Create main node
        self.draw_complex_node(center_x, center_y, 100, main_text)
        
        if sub_texts:
            # Create orbital paths
            num_orbits = min(len(sub_texts), 3)
            for i in range(num_orbits):
                angle = i * (2 * math.pi / num_orbits) - math.pi/2
                radius = 200 + i * 50
                
                # Calculate end point for this branch
                end_x = center_x + radius * math.cos(angle)
                end_y = center_y + radius * math.sin(angle)
                
                # Draw flowing connection
                self.draw_curved_connection(center_x, center_y, end_x, end_y)
                
                # Create secondary node
                self.draw_complex_node(end_x, end_y, 60, sub_texts[i])
                
                # Add branching paths
                if i < len(sub_texts) - 1:
                    self.create_branch_path(end_x, end_y, sub_texts[i+1])
                    
    def draw_complex_node(self, x, y, size, text):
        """Draw a detailed node with internal structure"""
        # Outer circle with rotating text
        self.canvas.create_oval(x-size, y-size, x+size, y+size, width=2)
        self.add_orbital_text(x, y, size * 0.9, text)
        
        # Inner concentric circles
        for i in range(1, 4):
            r = size * (0.8 - i * 0.2)
            self.canvas.create_oval(x-r, y-r, x+r, y+r, width=1)
        
        # Add circuit symbols in a circular pattern
        symbols = ['', '', '', '', '', '', '']
        for i, symbol in enumerate(symbols):
            angle = i * (2 * math.pi / len(symbols))
            sx = x + size * 0.5 * math.cos(angle)
            sy = y + size * 0.5 * math.sin(angle)
            self.canvas.create_text(sx, sy, text=symbol, font=('Segoe UI Symbol', 14))
            
        # Add central symbol
        self.canvas.create_text(x, y, text='', font=('Segoe UI Symbol', 20))
        
    def draw_curved_connection(self, start_x, start_y, end_x, end_y):
        """Draw an organic curved connection between nodes"""
        # Calculate control points for a natural curve
        dx = end_x - start_x
        dy = end_y - start_y
        
        # Create multiple control points for more organic flow
        ctrl1_x = start_x + dx * 0.25 - dy * 0.2
        ctrl1_y = start_y + dy * 0.25 + dx * 0.2
        ctrl2_x = start_x + dx * 0.75 + dy * 0.2
        ctrl2_y = start_y + dy * 0.75 - dx * 0.2
        
        # Draw the main curved path
        points = [start_x, start_y, ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, end_x, end_y]
        self.canvas.create_line(points, smooth=True, width=3)
        
        # Add orbital markers along the curve
        for t in range(1, 9):
            t = t / 10
            # Bezier curve calculation
            bx = self.bezier(t, start_x, ctrl1_x, ctrl2_x, end_x)
            by = self.bezier(t, start_y, ctrl1_y, ctrl2_y, end_y)
            self.canvas.create_text(bx, by, text='', font=('Segoe UI Symbol', 10))
            
    def create_branch_path(self, x, y, text):
        """Create smaller branching paths from a node"""
        num_branches = 3
        branch_length = 80
        
        for i in range(num_branches):
            angle = (i * 2 * math.pi / num_branches) + math.pi/6
            end_x = x + branch_length * math.cos(angle)
            end_y = y + branch_length * math.sin(angle)
            
            # Draw curved branch
            self.draw_curved_connection(x, y, end_x, end_y)
            
            # Add small terminal node
            self.draw_complex_node(end_x, end_y, 30, text)
            
    def add_orbital_text(self, x, y, radius, text):
        """Add text that follows a circular path"""
        chars = list(text + ' ' * 3)  # Add spacing between repetitions
        num_chars = len(chars)
        
        # Create multiple rotations of text
        for rotation in range(3):
            start_angle = rotation * (2 * math.pi / 3)
            for i, char in enumerate(chars):
                angle = start_angle + i * (2 * math.pi / (num_chars * 1.5))
                char_x = x + radius * math.cos(angle)
                char_y = y + radius * math.sin(angle)
                
                # Rotate each character to follow the circle
                char_angle = math.degrees(angle + math.pi/2)
                self.canvas.create_text(char_x, char_y, text=char,
                                     angle=char_angle, font=('TkFixedFont', 10))
                
    def bezier(self, t, p0, p1, p2, p3):
        """Calculate point on a cubic Bezier curve"""
        return (1-t)**3 * p0 + 3*(1-t)**2*t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3
