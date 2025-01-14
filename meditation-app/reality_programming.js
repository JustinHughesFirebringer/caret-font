// CARET Reality Programming Interface

class RealityProgrammer {
    constructor() {
        this.fieldStrength = 0;
        this.realitySync = 0;
        this.manifestationProgress = 0;
        this.activePatterns = null;
        
        this.initializeInterface();
        this.setupEventListeners();
    }

    initializeInterface() {
        // Initialize rotating patterns
        gsap.to('.rotating-slow', {
            rotation: 360,
            duration: 60,
            repeat: -1,
            ease: 'none'
        });

        gsap.to('.rotating-medium', {
            rotation: -360,
            duration: 40,
            repeat: -1,
            ease: 'none'
        });

        gsap.to('.rotating-fast', {
            rotation: 360,
            duration: 20,
            repeat: -1,
            ease: 'none'
        });

        // Initialize central node pulsing
        gsap.to('.central-node', {
            scale: 1.2,
            duration: 2,
            repeat: -1,
            yoyo: true,
            ease: 'power1.inOut'
        });
    }

    setupEventListeners() {
        const startBtn = document.getElementById('startBtn');
        const manifestationType = document.getElementById('manifestation-type');

        startBtn.addEventListener('click', () => this.initializeProgram(manifestationType.value));
    }

    async initializeProgram(type) {
        const startBtn = document.getElementById('startBtn');
        startBtn.disabled = true;
        startBtn.textContent = 'Initializing Fields...';

        try {
            const response = await fetch('http://localhost:8000/program', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    type: type,
                    target_state: this.getTargetState(type)
                })
            });

            const data = await response.json();
            this.updateInterface(data);
            this.activatePatterns(data.active_patterns);
        } catch (error) {
            console.error('Reality programming error:', error);
            this.handleError();
        }
    }

    getTargetState(type) {
        const states = {
            'wealth': {
                field_type: 'abundance',
                intensity: 1.0,
                persistence: 0.95
            },
            'health': {
                field_type: 'vitality',
                intensity: 1.0,
                persistence: 0.95
            },
            'custom': {
                field_type: 'general',
                intensity: 0.8,
                persistence: 0.9
            }
        };
        return states[type] || states.custom;
    }

    updateInterface(data) {
        const fieldStrength = document.querySelector('#field-strength span');
        const realitySync = document.querySelector('#reality-sync span');
        const manifestationProgress = document.querySelector('#manifestation-progress span');

        fieldStrength.textContent = `${Math.round(data.field_strength * 100)}%`;
        realitySync.textContent = `${Math.round(data.reality_sync * 100)}%`;
        manifestationProgress.textContent = data.estimated_completion;

        this.updatePatternIntensity(data.field_strength);
    }

    updatePatternIntensity(strength) {
        const patterns = document.querySelectorAll('.glyph');
        patterns.forEach(pattern => {
            pattern.style.opacity = 0.3 + (strength * 0.7);
        });
    }

    activatePatterns(patterns) {
        // Activate state definition pattern
        this.setPatternText('.state-definition textPath', patterns.state);
        
        // Activate field generation pattern
        this.setPatternText('.field-generation textPath', patterns.field);
        
        // Activate reality interface pattern
        this.setPatternText('.reality-interface textPath', patterns.interface);
        
        // Enhance rotation speeds based on activation
        this.enhanceRotations();
    }

    setPatternText(selector, text) {
        const element = document.querySelector(selector);
        if (element) {
            element.textContent = `${text} ${text} ${text}`;
        }
    }

    enhanceRotations() {
        gsap.to('.rotating-slow', {
            duration: 30,
            ease: 'power1.inOut'
        });

        gsap.to('.rotating-medium', {
            duration: 20,
            ease: 'power1.inOut'
        });

        gsap.to('.rotating-fast', {
            duration: 10,
            ease: 'power1.inOut'
        });
    }

    handleError() {
        const startBtn = document.getElementById('startBtn');
        startBtn.disabled = false;
        startBtn.textContent = 'Reality Programming Failed - Retry';
        
        const manifestationProgress = document.querySelector('#manifestation-progress span');
        manifestationProgress.textContent = 'Error - Field Collapse';
    }
}

// Initialize Reality Programmer when document loads
document.addEventListener('DOMContentLoaded', () => {
    window.realityProgrammer = new RealityProgrammer();
});
