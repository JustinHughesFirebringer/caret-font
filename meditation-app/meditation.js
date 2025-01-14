class MeditationApp {
    constructor() {
        this.audioContext = null;
        this.audioElement = null;
        this.currentState = 'preparation';
        this.patternContainer = document.getElementById('pattern-container');
        this.progressBar = document.getElementById('progress-bar');
        this.timeDisplay = document.getElementById('time-display');
        this.stateIndicator = document.getElementById('state-indicator');
        this.startButton = document.getElementById('startBtn');
        this.volumeControl = document.getElementById('volume');

        // State timing in seconds
        this.states = {
            alpha: { duration: 660, name: 'Alpha - Progressive Relaxation' },  // 11 minutes
            theta: { duration: 300, name: 'Theta - Visualization' },          // 5 minutes
            delta: { duration: 300, name: 'Delta - Pure Receiving' }          // 5 minutes
        };

        this.totalDuration = Object.values(this.states)
            .reduce((total, state) => total + state.duration, 0);

        this.setupEventListeners();
        this.loadPatterns();
    }

    loadPatterns() {
        // Store SVG patterns
        this.patterns = {
            alpha: document.getElementById('alpha-pattern-svg').innerHTML,
            theta: document.getElementById('theta-pattern-svg').innerHTML,
            delta: document.getElementById('delta-pattern-svg').innerHTML
        };

        // Set initial pattern
        this.patternContainer.innerHTML = document.querySelector('#pattern-container svg').outerHTML;
    }

    setupEventListeners() {
        this.startButton.addEventListener('click', () => this.startMeditation());
        this.volumeControl.addEventListener('input', (e) => {
            if (this.audioElement) {
                this.audioElement.volume = e.target.value;
            }
        });
    }

    createAudioElement() {
        this.audioElement = document.createElement('audio');
        this.audioElement.id = 'guided-meditation';
        this.audioElement.src = 'http://localhost:8000/audio/MoneyMeditation.mp3';
        this.audioElement.preload = 'auto';
        document.body.appendChild(this.audioElement);
    }

    async startMeditation() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }

        if (!this.audioElement) {
            this.createAudioElement();
        }

        try {
            await this.audioElement.play();
            this.startButton.disabled = true;
            this.startButton.textContent = 'Meditation in Progress...';
            this.updateProgress();
            this.startStateTransitions();
        } catch (error) {
            console.error('Error playing audio:', error);
            this.startButton.textContent = 'Error - Try Again';
            this.startButton.disabled = false;
        }
    }

    updateProgress() {
        if (!this.audioElement) return;

        const currentTime = this.audioElement.currentTime;
        const duration = this.totalDuration;
        const progress = (currentTime / duration) * 100;
        
        this.progressBar.style.width = `${progress}%`;
        
        // Update time display
        const remainingSeconds = duration - currentTime;
        const minutes = Math.floor(remainingSeconds / 60);
        const seconds = Math.floor(remainingSeconds % 60);
        this.timeDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

        if (currentTime < duration) {
            requestAnimationFrame(() => this.updateProgress());
        } else {
            this.endMeditation();
        }
    }

    startStateTransitions() {
        let elapsedTime = 0;
        
        // Alpha state (0-11 minutes)
        setTimeout(() => {
            this.transitionToState('alpha');
        }, elapsedTime * 1000);
        
        // Theta state (11-16 minutes)
        elapsedTime += this.states.alpha.duration;
        setTimeout(() => {
            this.transitionToState('theta');
        }, elapsedTime * 1000);
        
        // Delta state (16-21 minutes)
        elapsedTime += this.states.theta.duration;
        setTimeout(() => {
            this.transitionToState('delta');
        }, elapsedTime * 1000);
    }

    transitionToState(state) {
        // Update state indicator
        this.stateIndicator.textContent = `Current State: ${this.states[state].name}`;
        
        // Fade out current pattern
        gsap.to(this.patternContainer, {
            opacity: 0,
            duration: 1,
            onComplete: () => {
                // Update pattern
                this.patternContainer.innerHTML = this.patterns[state];
                
                // Fade in new pattern
                gsap.to(this.patternContainer, {
                    opacity: 1,
                    duration: 1
                });
            }
        });

        // Add animation to the pattern
        gsap.to(`#${state}-pattern-svg svg`, {
            rotation: 360,
            duration: 60,
            repeat: -1,
            ease: "none"
        });

        this.updatePattern(state.toUpperCase());
    }

    updatePattern(state) {
        const patternContainer = document.getElementById('pattern-container');
        let patternSvg;
        
        switch(state) {
            case 'ALPHA':
                patternSvg = document.getElementById('alpha-pattern-svg').innerHTML;
                gsap.to(patternContainer, {
                    opacity: 0,
                    duration: 1,
                    onComplete: () => {
                        patternContainer.innerHTML = patternSvg;
                        gsap.to(patternContainer, {
                            opacity: 1,
                            duration: 1,
                            onComplete: () => {
                                this.activateHealthCircuit();
                            }
                        });
                    }
                });
                break;
            case 'THETA':
                patternSvg = document.getElementById('theta-pattern-svg').innerHTML;
                gsap.to(patternContainer, {
                    opacity: 0,
                    duration: 1,
                    onComplete: () => {
                        patternContainer.innerHTML = patternSvg;
                        gsap.to(patternContainer, {
                            opacity: 1,
                            duration: 1,
                            onComplete: () => {
                                this.activateWealthCircuit();
                            }
                        });
                    }
                });
                break;
            case 'DELTA':
                patternSvg = document.getElementById('delta-pattern-svg').innerHTML;
                gsap.to(patternContainer, {
                    opacity: 0,
                    duration: 1,
                    onComplete: () => {
                        patternContainer.innerHTML = patternSvg;
                        gsap.to(patternContainer, {
                            opacity: 1,
                            duration: 1,
                            onComplete: () => {
                                this.activateWisdomCircuit();
                            }
                        });
                    }
                });
                break;
        }
    }

    activateHealthCircuit() {
        const dnaHelix = document.querySelector('.dna-helix');
        const glyphNodes = document.querySelectorAll('.glyph-nodes');
        
        gsap.fromTo(dnaHelix, 
            { scale: 0.8, opacity: 0 },
            { scale: 1, opacity: 1, duration: 2, ease: "power2.out" }
        );
        
        glyphNodes.forEach((node, index) => {
            gsap.fromTo(node,
                { opacity: 0, y: 20 },
                { 
                    opacity: 1, 
                    y: 0, 
                    duration: 1,
                    delay: index * 0.2,
                    ease: "back.out(1.7)"
                }
            );
        });
    }

    activateWealthCircuit() {
        const abundanceFlow = document.querySelector('.abundance-flow');
        const prosperityNodes = document.querySelectorAll('.prosperity-nodes circle');
        
        gsap.fromTo(abundanceFlow,
            { strokeDashoffset: 1000 },
            { 
                strokeDashoffset: 0,
                duration: 3,
                ease: "power2.inOut"
            }
        );
        
        prosperityNodes.forEach((node, index) => {
            gsap.fromTo(node,
                { scale: 0, opacity: 0 },
                { 
                    scale: 1,
                    opacity: 1,
                    duration: 1,
                    delay: index * 0.3,
                    ease: "elastic.out(1, 0.5)"
                }
            );
        });
    }

    activateWisdomCircuit() {
        const wisdomEye = document.querySelector('.wisdom-eye');
        const wisdomRays = document.querySelector('.wisdom-rays');
        const insightNodes = document.querySelector('.insight-nodes');
        
        gsap.fromTo(wisdomEye,
            { scale: 0.5, opacity: 0 },
            { 
                scale: 1,
                opacity: 1,
                duration: 2,
                ease: "power3.out"
            }
        );
        
        gsap.fromTo(wisdomRays,
            { rotation: -30, opacity: 0 },
            { 
                rotation: 0,
                opacity: 1,
                duration: 2,
                delay: 0.5,
                ease: "power2.out"
            }
        );
        
        gsap.fromTo(insightNodes,
            { scale: 0.8, opacity: 0 },
            { 
                scale: 1,
                opacity: 1,
                duration: 1.5,
                delay: 1,
                ease: "back.out(1.7)"
            }
        );
    }

    endMeditation() {
        this.startButton.disabled = false;
        this.startButton.textContent = 'Begin Money Meditation Journey';
        this.stateIndicator.textContent = 'Meditation Complete';
        
        if (this.audioElement) {
            this.audioElement.pause();
            this.audioElement.currentTime = 0;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const audioPlayer = document.getElementById('audio-player');
    const playBtn = document.getElementById('play-btn');
    const stopBtn = document.getElementById('stop-btn');
    const symbolButtons = document.querySelectorAll('.symbol-btn');
    
    let currentAudioUrl = null;
    const sequence = ['⎍', '⎎', '⎏', '⎐', '⎑', '⎒', '⎓', '⎔', '⎕'];
    let isPlaying = false;

    // Function to highlight current symbol
    function highlightSymbol(symbol) {
        symbolButtons.forEach(btn => {
            if (btn.dataset.symbol === symbol) {
                btn.style.background = 'rgba(255, 255, 255, 0.3)';
            } else {
                btn.style.background = 'rgba(255, 255, 255, 0.15)';
            }
        });
    }

    // Function to play the full sequence
    async function playSequence(manifestation = null) {
        if (isPlaying) return;
        
        isPlaying = true;
        playBtn.disabled = true;
        stopBtn.disabled = false;

        try {
            const response = await fetch('/generate_sequence', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    symbols: sequence,
                    manifestation: manifestation
                })
            });

            if (!response.ok) {
                throw new Error('Failed to generate audio sequence');
            }

            const audioBlob = await response.blob();
            
            // Clean up previous audio URL if it exists
            if (currentAudioUrl) {
                URL.revokeObjectURL(currentAudioUrl);
            }
            
            currentAudioUrl = URL.createObjectURL(audioBlob);
            audioPlayer.src = currentAudioUrl;
            audioPlayer.load();
            
            // Start playback
            audioPlayer.play();
            
            // Setup timing for symbol highlights
            const intervalTime = 3000; // 3 seconds per symbol
            let currentIndex = 0;
            
            const highlightInterval = setInterval(() => {
                if (currentIndex < sequence.length) {
                    highlightSymbol(sequence[currentIndex]);
                    currentIndex++;
                } else {
                    clearInterval(highlightInterval);
                }
            }, intervalTime);
            
        } catch (error) {
            console.error('Error playing sequence:', error);
            alert('Failed to play sequence. Please try again.');
            isPlaying = false;
            playBtn.disabled = false;
            stopBtn.disabled = true;
        }
    }

    // Play button handler
    playBtn.addEventListener('click', () => {
        playSequence();
    });

    // Stop button handler
    stopBtn.addEventListener('click', () => {
        audioPlayer.pause();
        audioPlayer.currentTime = 0;
        isPlaying = false;
        playBtn.disabled = false;
        stopBtn.disabled = true;
        
        // Reset all button styles
        symbolButtons.forEach(btn => {
            btn.style.background = 'rgba(255, 255, 255, 0.15)';
        });
    });

    // Audio player event handlers
    audioPlayer.addEventListener('ended', () => {
        audioPlayer.currentTime = 0;
        isPlaying = false;
        playBtn.disabled = false;
        stopBtn.disabled = true;
        
        // Reset all button styles
        symbolButtons.forEach(btn => {
            btn.style.background = 'rgba(255, 255, 255, 0.15)';
        });
    });

    // Clean up function for audio URLs
    window.addEventListener('beforeunload', () => {
        if (currentAudioUrl) {
            URL.revokeObjectURL(currentAudioUrl);
        }
    });
    
    // Enable play button initially
    playBtn.disabled = false;
    
    const app = new MeditationApp();
});
