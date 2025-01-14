from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import mimetypes
import json
from datetime import datetime
import math
from flask import Flask, send_file, jsonify, request
import numpy as np
from scipy.io import wavfile
import io

app = Flask(__name__)

class RealityProgrammingHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle regular file serving
        return SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/program':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                response = self.process_reality_program(data)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            return

        self.send_error(404)

    def process_reality_program(self, data):
        """Process reality programming request using CARET system"""
        program_type = data.get('type', 'custom')
        target_state = data.get('target_state', {})
        
        # Calculate field strengths based on CARET patterns
        state_field = self.calculate_state_field(program_type, target_state)
        reality_field = self.calculate_reality_field(state_field)
        manifestation_probability = self.calculate_manifestation(reality_field)
        
        return {
            'field_strength': state_field,
            'reality_sync': reality_field,
            'manifestation_probability': manifestation_probability,
            'estimated_completion': self.estimate_completion(manifestation_probability),
            'active_patterns': self.get_active_patterns(program_type)
        }

    def calculate_state_field(self, program_type, target_state):
        """Calculate state definition field strength"""
        base_patterns = {
            'wealth': {
                'primary': ['⌘⌬⌭⌮⌦', '⊢⊣∩∪', '⌸⌹⌺'],
                'amplifiers': ['⊕⊗⊘', '⊞⊟⊠', '⊸⊹⊺'],
                'resonators': ['⋈⋉⋊', '⋎⋏⋐', '⋮⋯⋰']
            },
            'health': {
                'primary': ['⌘⌬⌭⌮⌦', '⊢⊣∩∪', '⌸⌹⌺'],
                'amplifiers': ['⊕⊗⊘', '⊞⊟⊠', '⊸⊹⊺'],
                'resonators': ['⋈⋉⋊', '⋎⋏⋐', '⋮⋯⋰']
            },
            'custom': {
                'primary': ['⌘⌬⌭⌮⌦', '⊢⊣∩∪', '⌸⌹⌺'],
                'amplifiers': ['⊕⊗⊘', '⊞⊟⊠', '⊸⊹⊺'],
                'resonators': ['⋈⋉⋊', '⋎⋏⋐', '⋮⋯⋰']
            }
        }
        
        patterns = base_patterns.get(program_type, base_patterns['custom'])
        
        # Calculate primary pattern strength
        primary_strength = sum(len(p) for p in patterns['primary']) * 0.15
        
        # Calculate amplification factor
        amplification = sum(len(p) for p in patterns['amplifiers']) * 0.2
        
        # Calculate resonance factor
        resonance = sum(len(p) for p in patterns['resonators']) * 0.25
        
        # Combine all factors with geometric enhancement
        field_strength = (primary_strength * (1 + amplification)) * (1 + resonance)
        
        # Apply quantum coupling factor
        quantum_coupling = math.sin(field_strength * math.pi / 2) ** 2
        
        # Return enhanced field strength
        return min(field_strength * (1 + quantum_coupling), 1.0)

    def calculate_reality_field(self, state_field):
        """Calculate reality interface field strength"""
        # Enhanced quantum field equations
        reality_coupling = math.sin(state_field * math.pi / 2) ** 2
        field_coherence = 1 - math.exp(-2 * state_field)
        quantum_resonance = math.cos(state_field * math.pi / 4) ** 2
        
        # Combine factors with weighted importance
        field_strength = (
            reality_coupling * 0.4 +
            field_coherence * 0.4 +
            quantum_resonance * 0.2
        )
        
        return field_strength

    def calculate_manifestation(self, reality_field):
        """Calculate manifestation probability"""
        return reality_field ** 2 * 100

    def estimate_completion(self, probability):
        """Estimate completion timeframe"""
        if probability > 90:
            return "Immediate"
        elif probability > 70:
            return "Within 24 hours"
        elif probability > 50:
            return "Within 3 days"
        else:
            return "Requires pattern strengthening"

    def get_active_patterns(self, program_type):
        """Get active CARET patterns for the program type"""
        patterns = {
            'wealth': {
                'state': '⌘⌬⌭⌮⌦⊕⊗⊘',
                'field': '⊢⊣∩∪⍉⍊⍋⊞⊟⊠',
                'interface': '⌸⌹⌺⍁⍂⍃⌲⌳⌴⊸⊹⊺'
            },
            'health': {
                'state': '⌘⌬⌭⌮⌦⊕⊗⊘',
                'field': '⊢⊣∩∪⍉⍊⍋⊞⊟⊠',
                'interface': '⌸⌹⌺⍁⍂⍃⌲⌳⌴⊸⊹⊺'
            },
            'custom': {
                'state': '⌘⌬⌭⌮⌦⊕⊗⊘',
                'field': '⊢⊣∩∪⍉⍊⍋⊞⊟⊠',
                'interface': '⌸⌹⌺⍁⍂⍃⌲⌳⌴⊸⊹⊺'
            }
        }
        return patterns.get(program_type, patterns['custom'])

# Frequency mapping
FREQUENCIES = {
    '⎍': 396,  # Open Activation
    '⎎': 417,  # Open Flow
    '⎏': 528,  # Open Terminal
    '⎐': 639,  # Flow Activation
    '⎑': 741,  # Flow Flow
    '⎒': 852,  # Flow Terminal
    '⎓': 285,  # Close Activation
    '⎔': 174,  # Close Flow
    '⎕': 963   # Close Terminal
}

def generate_tone(frequency, duration=3, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(2 * np.pi * frequency * t)
    # Apply fade in/out
    fade_duration = 0.1  # seconds
    fade_length = int(fade_duration * sample_rate)
    fade_in = np.linspace(0, 1, fade_length)
    fade_out = np.linspace(1, 0, fade_length)
    tone[:fade_length] *= fade_in
    tone[-fade_length:] *= fade_out
    return tone

def generate_sequence(symbols, manifestation=None):
    sample_rate = 44100
    duration_per_tone = 3  # seconds
    crossfade_duration = 0.5  # seconds
    
    # Calculate total samples needed
    total_duration = len(symbols) * duration_per_tone
    total_samples = int(total_duration * sample_rate)
    combined_audio = np.zeros(total_samples)
    
    for i, symbol in enumerate(symbols):
        if symbol not in FREQUENCIES:
            continue
            
        frequency = FREQUENCIES[symbol]
        tone = generate_tone(frequency, duration_per_tone, sample_rate)
        
        # Calculate start position for this tone
        start_pos = i * duration_per_tone * sample_rate
        end_pos = start_pos + len(tone)
        
        # Add the tone to the combined audio
        combined_audio[start_pos:end_pos] += tone
        
        # Add manifestation after Open Terminal (⎏)
        if symbol == '⎏' and manifestation:
            # Generate a special manifestation tone (using 528 Hz as base)
            manifestation_tone = generate_tone(528, 1.5, sample_rate)
            manifest_start = end_pos - int(0.5 * sample_rate)  # Overlap slightly
            manifest_end = manifest_start + len(manifestation_tone)
            combined_audio[manifest_start:manifest_end] += manifestation_tone * 0.5  # Lower volume for manifestation
    
    # Normalize the audio
    combined_audio = np.clip(combined_audio, -1, 1)
    return combined_audio

@app.route('/generate_sequence', methods=['POST'])
def generate_sequence_audio():
    data = request.get_json()
    symbols = data.get('symbols', [])
    manifestation = data.get('manifestation')
    
    audio_data = generate_sequence(symbols, manifestation)
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Create a BytesIO object to store the WAV file
    buffer = io.BytesIO()
    wavfile.write(buffer, 44100, audio_data)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='audio/wav',
        as_attachment=True,
        download_name='meditation_sequence.wav'
    )

@app.route('/generate_audio/<symbol>')
def generate_audio(symbol):
    if symbol not in FREQUENCIES:
        return jsonify({'error': 'Invalid symbol'}), 400
    
    frequency = FREQUENCIES[symbol]
    audio_data = generate_tone(frequency)
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Create a BytesIO object to store the WAV file
    buffer = io.BytesIO()
    wavfile.write(buffer, 44100, audio_data)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='audio/wav',
        as_attachment=True,
        download_name=f'tone_{frequency}hz.wav'
    )

@app.route('/')
def index():
    return app.send_static_file('index.html')

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RealityProgrammingHandler)
    print(f'Starting CARET Reality Programming server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    app.run(debug=True)
