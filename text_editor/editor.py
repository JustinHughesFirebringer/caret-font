import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from fractal_glyphs import FractalGlyphRenderer

class DualFontEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("CARET Text Editor")
        
        # Configure main window
        self.root.geometry("1200x800")
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create toolbar
        self.toolbar = ttk.Frame(self.main_frame)
        self.toolbar.pack(fill='x', pady=(0, 5))
        self.create_toolbar()
        
        # Create horizontal paned window for split layout
        self.paned_window = ttk.PanedWindow(self.main_frame, orient='horizontal')
        self.paned_window.pack(expand=True, fill='both')
        
        # Left side - Text Editor and Canvas Container
        self.left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, weight=3)
        
        # Create canvas for fractal glyphs (hidden initially)
        self.glyph_canvas = tk.Canvas(self.left_frame, width=800, height=600)
        self.glyph_renderer = FractalGlyphRenderer(self.glyph_canvas)
        
        # Create text area
        self.text_area = scrolledtext.ScrolledText(
            self.left_frame,
            wrap=tk.WORD,
            width=40,
            height=20,
            font=("Segoe UI Symbol", 12),  # Start with a known good font
            spacing1=5,
            spacing2=2,
            spacing3=5,
            padx=10,
            pady=10
        )
        self.text_area.pack(expand=True, fill='both')
        
        # Right side - Character Map
        self.charmap_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.charmap_frame, weight=1)
        
        # Create character map
        self.create_character_map()
        
        # Bind key events
        self.text_area.bind('<Key>', self.on_key_press)
        
    def create_character_map(self):
        """Create character map in the right pane"""
        # Create notebook for tabs
        self.char_map_notebook = ttk.Notebook(self.charmap_frame)
        self.char_map_notebook.pack(expand=True, fill='both')
        
        # Create frames for different character categories
        frames = {
            'Primary Matrix': ttk.Frame(self.char_map_notebook),
            'Circuit Elements': ttk.Frame(self.char_map_notebook),
            'State Markers': ttk.Frame(self.char_map_notebook),
            'Flight Control': ttk.Frame(self.char_map_notebook),
            'Special Symbols': ttk.Frame(self.char_map_notebook)
        }
        
        # Add frames to notebook
        for name, frame in frames.items():
            self.char_map_notebook.add(frame, text=name)
        
        # Complete character mappings by category
        char_groups = {
            'Primary Matrix': {
                'v': '⎮', 'V': '⎢', '[': '⎜', ']': '⎮', '|': '⎸',
                't': '⎧', 'T': '⎡', '(': '⎛', ')': '⎞', '{': '⎰',
                '}': '⎱', '<': '⎴', '>': '⎵', 'b': '⎩', 'B': '⎣',
                '\\': '⎝', '/': '⎠', '-': '⎯', '=': '⎺', '_': '⎽',
                '+': '⎶', 'p': '⎨', 'P': '⎥', 'e': '⎪', 'E': '⎦'
            },
            'Circuit Elements': {
                '1': '⎍', '2': '⎎', '3': '⎏',  # Circuit Open
                '4': '⎐', '5': '⎑', '6': '⎒',  # Circuit Flow
                '7': '⎓', '8': '⎔', '9': '⎕',  # Circuit Close
                'n1': '⊕', 'n2': '⊗', 'n3': '⊘',
                'n4': '⊙', 'n5': '⊚', 'n6': '⊛',
                'n7': '⊜', 'n8': '⊝'
            },
            'State Markers': {
                'q': '⎚', 'w': '⎛', 'r': '⎜',  # Alpha
                'a': '⎝', 's': '⎞', 'd': '⎟',  # Theta
                'z': '⎠', 'x': '⎡', 'c': '⎢',  # Delta
                'm1': '▷', 'm2': '▹', 'm3': '⊢',
                'm4': '∨', 'm5': '⊤', 'm6': '⊥'
            },
            'Flight Control': {
                'F1': '⌋', 'F2': '∇', 'F3': '⊢',
                'F4': '⊣', 'F5': '⊤', 'F6': '∩',
                'F7': '⌈', 'F8': '∆', 'F9': '⊥',
                'F10': '⊦', 'F11': '⊧', 'F12': '∪'
            },
            'Special Symbols': {
                'c1': '⬡', 'c2': '⚡', 'c3': '⟳',
                'c4': '≡', 'c5': '∥', 'c6': '⟲',
                'r1': '⌁', 'r2': '⊕', 'r3': '∧',
                'r4': '∨', 'r5': '⟨', 'r6': '⟩',
                'x1': '⊞', 'x2': '⊟', 'x3': '⊠',
                'x4': '⊡', 'x5': '⊚', 'x6': '⊛'
            }
        }
        
        # Populate each frame
        for name, chars in char_groups.items():
            self.populate_char_map(frames[name], chars)
            
    def populate_char_map(self, frame, char_dict):
        """Populate character map with better spacing"""
        row = 0
        col = 0
        max_cols = 4  # Reduced number of columns for better visibility
        
        # Configure grid weights for better spacing
        for i in range(max_cols):
            frame.grid_columnconfigure(i, weight=1, minsize=60)
        
        for key, char in char_dict.items():
            # Create button frame for better organization
            btn_frame = ttk.Frame(frame, padding=5)
            btn_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            # Create button with larger size
            btn = ttk.Button(
                btn_frame,
                text=char,
                width=6,  # Increased width
                command=lambda c=char: self.insert_char(c)
            )
            btn.pack(pady=2, expand=True, fill='both')
            
            # Add key binding label
            ttk.Label(btn_frame, text=f"[{key}]").pack()
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
    def insert_char(self, char):
        """Insert character with proper Unicode handling"""
        try:
            # Ensure proper Unicode encoding
            if isinstance(char, str):
                char = char.encode('utf-8').decode('utf-8')
            current_pos = self.text_area.index(tk.INSERT)
            self.text_area.insert(current_pos, char)
        except Exception as e:
            print(f"Error inserting character: {e}")
        
    def on_key_press(self, event):
        if self.font_var.get() == "CARET":
            # Handle function keys for flight control characters
            if event.keysym.startswith('F'):
                if event.keysym in self.caret_map:
                    self.insert_char(self.caret_map[event.keysym])
                    return "break"
            # Handle regular character mappings
            elif event.char in self.caret_map:
                self.insert_char(self.caret_map[event.char])
                return "break"
                
    def toggle_font(self):
        current_text = self.text_area.get("1.0", tk.END)
        if self.font_var.get() == "Standard":
            self.text_area.configure(font=("TkDefaultFont", 12))
        else:
            # Use the Unicode-compatible font when in CARET mode
            self.text_area.configure(font=("Segoe UI Symbol", 12))
            
    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        
    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
                
    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(file_path, 'w') as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
                
    def create_new_glyph(self):
        """Create new glyph from selected text or all text"""
        try:
            text = self.text_area.get("sel.first", "sel.last")
        except tk.TclError:
            text = self.text_area.get("1.0", tk.END)
        
        text = text.strip()
        if text:
            self.toggle_canvas()  # Switch to canvas view
            self.glyph_renderer.create_glyph_from_text(text)
            
    def toggle_canvas(self):
        """Toggle between text editor and glyph canvas"""
        if self.glyph_canvas.winfo_ismapped():
            self.glyph_canvas.pack_forget()
            self.text_area.pack(expand=True, fill='both')
        else:
            text_content = self.text_area.get("1.0", tk.END).strip()
            self.text_area.pack_forget()
            self.glyph_canvas.pack(expand=True, fill='both')
            
            if text_content:
                self.glyph_renderer.create_glyph_from_text(text_content)
                
    def create_toolbar(self):
        """Create toolbar with buttons"""
        # Font selection
        ttk.Label(self.toolbar, text="Font:").pack(side=tk.LEFT, padx=5)
        self.font_var = tk.StringVar(value="Standard")
        font_menu = ttk.OptionMenu(self.toolbar, self.font_var, "Standard", "Standard", "CARET")
        font_menu.pack(side=tk.LEFT, padx=5)
        
        # Add buttons
        ttk.Button(self.toolbar, text="Toggle Font", 
                  command=self.toggle_font).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="New Fractal Glyph", 
                  command=self.create_new_glyph).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.toolbar, text="Toggle Canvas", 
                  command=self.toggle_canvas).pack(side=tk.LEFT, padx=5)
                  
    def caret_map(self):
        # CARET character mappings
        self.caret_map = {
            # Primary Matrix - Energy Flow
            'v': '⎪', 'V': '⎢', '[': '⎜', ']': '⎮', '|': '⎸',
            't': '⎧', 'T': '⎡', '(': '⎛', '{': '⎰', '<': '⎴',
            'b': '⎩', 'B': '⎣', ')': '⎝', '}': '⎱', '>': '⎵',
            'p': '⎨', 'P': '⎥', '\\': '⎟', '-': '⎲', '=': '⎶',
            'e': '⎪', 'E': '⎦', '/': '⎠', '_': '⎳', '+': '⎷',
            
            # Central Node Characters
            'n1': '⊕', 'n2': '⊗', 'n3': '⊘', 'n4': '⊙',
            'n5': '⊚', 'n6': '⊛', 'n7': '⊜', 'n8': '⊝',
            
            # Circumferential Text
            'c1': '⬡', 'c2': '⚡', 'c3': '⟳', 'c4': '≡',
            'c5': '∥', 'c6': '⟲',
            
            # Ring Text
            'r1': '⌁', 'r2': '⊕', 'r3': '∧', 'r4': '∨',
            'r5': '⟨', 'r6': '⟩',
            
            # Radial Markers
            'm1': '▷', 'm2': '▹', 'm3': '⊢', 'm4': '∨',
            'm5': '⊤', 'm6': '⊥',
            
            # Connection Text
            'x1': '⊞', 'x2': '⊟', 'x3': '⊠', 'x4': '⊡',
            'x5': '⊚', 'x6': '⊛', 'x7': '⊕', 'x8': '⊗',
            
            # Linear Connectors
            'l1': '⟨', 'l2': '⟩', 'l3': '⟪', 'l4': '⟫',
            'l5': '∧', 'l6': '≡',
            
            # Junction Characters
            'j1': '∨', 'j2': '∧', 'j3': '⊆', 'j4': '⊇',
            'j5': '∩', 'j6': '∪',
            
            # Boundary Indicators
            'b1': '⋮', 'b2': '⋯', 'b3': '∴', 'b4': '∵',
            
            # Complex Form Elements
            'f1': '✻', 'f2': '⊘', 'f3': '⟲',
            
            # Field Effect Indicators
            'i1': '⟜', 'i2': '⊥', 'i3': '⊤', 'i4': '∨',
            'i5': '∧', 'i6': '∇',
            
            # Special Combinations (accessible via Alt key)
            'Alt-1': '⊞⊟⊠⊡',  # Field Indicators
            'Alt-2': '⊚⊥⊢⊣',  # State Markers
            'Alt-3': '⊤⊕⊗⊘',  # Additional State Markers
            
            # Circuit Elements
            '1': '⎍', '2': '⎎', '3': '⎏',  # Circuit Open
            '4': '⎐', '5': '⎑', '6': '⎒',  # Circuit Flow
            '7': '⎓', '8': '⎔', '9': '⎕',  # Circuit Close
            
            # State Markers
            'q': '⎚', 'w': '⎛', 'r': '⎜',  # Alpha
            'a': '⎝', 's': '⎞', 'd': '⎟',  # Theta
            'z': '⎠', 'x': '⎡', 'c': '⎢',  # Delta
            
            # Flight Control - Primary Sequence
            'F1': '⌋', 'F2': '∇', 'F3': '⊢',
            'F4': '⊣', 'F5': '⊤', 'F6': '∩',
            
            # Flight Control - Secondary Sequence
            'F7': '⌈', 'F8': '∆', 'F9': '⊥',
            'F10': '⊦', 'F11': '⊧', 'F12': '∪',
            
            # Additional Transformations
            'f': '⎤', 'g': '⎥', 'h': '⎦',  # State termination
            'j': '⎧', 'k': '⎨', 'l': '⎩',  # Energy circuit
            'y': '⎮', 'u': '⎯', 'i': '⎰',  # Field maintenance
            'm': '⎱', 'n': '⎲', 'o': '⎳',  # Process flow
            ',': '⎴', '.': '⎵', '/': '⎶',  # Interface bridge
            ';': '⎷', ':': '⎸', "'": '⎹'   # Reality anchor
        }
        
if __name__ == "__main__":
    root = tk.Tk()
    editor = DualFontEditor(root)
    root.mainloop()
