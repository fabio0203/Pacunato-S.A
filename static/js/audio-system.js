// ============================================
// SISTEMA DE AUDIO CINEMATOGRÁFICO
// ============================================

class AudioSystem {
    constructor() {
        this.sounds = {};
        this.audioContext = null;
        this.masterGain = null;
        this.musicGain = null;
        this.sfxGain = null;
        this.isInitialized = false;
        this.isMuted = false;
        this.activeOscillators = []; // NUEVO: Para trackear osciladores activos
        
        // Configuración de volumen
        this.volumes = {
            master: 0.7,
            music: 0.3,
            sfx: 0.6
        };
    }
    
    async init() {
        // Crear Audio Context
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // Crear nodos de ganancia (volumen)
        this.masterGain = this.audioContext.createGain();
        this.musicGain = this.audioContext.createGain();
        this.sfxGain = this.audioContext.createGain();
        
        // Conectar nodos
        this.musicGain.connect(this.masterGain);
        this.sfxGain.connect(this.masterGain);
        this.masterGain.connect(this.audioContext.destination);
        
        // Establecer volúmenes
        this.masterGain.gain.value = this.volumes.master;
        this.musicGain.gain.value = this.volumes.music;
        this.sfxGain.gain.value = this.volumes.sfx;
        
        // Crear sonidos sintéticos
        this.createSyntheticSounds();
        
        this.isInitialized = true;
    }
    
    createSyntheticSounds() {
        this.sounds = {
            startup: () => this.playStartupSound(),
            progress: () => this.playProgressSound(),
            stage: () => this.playStageSound(),
            complete: () => this.playCompleteSound(),
            whoosh: () => this.playWhooshSound(),
            glitch: () => this.playGlitchSound(),
            ambient: () => this.playAmbientMusic()
        };
    }
    
    // ============================================
    // SONIDOS SINTÉTICOS
    // ============================================
    
    playStartupSound() {
        const now = this.audioContext.currentTime;
        
        // Oscilador 1 - Tono bajo que sube
        const osc1 = this.audioContext.createOscillator();
        const gain1 = this.audioContext.createGain();
        
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(100, now);
        osc1.frequency.exponentialRampToValueAtTime(400, now + 1);
        
        gain1.gain.setValueAtTime(0, now);
        gain1.gain.linearRampToValueAtTime(0.3, now + 0.1);
        gain1.gain.exponentialRampToValueAtTime(0.01, now + 1.5);
        
        osc1.connect(gain1);
        gain1.connect(this.sfxGain);
        
        osc1.start(now);
        osc1.stop(now + 1.5);
        
        // Oscilador 2 - Armónico
        const osc2 = this.audioContext.createOscillator();
        const gain2 = this.audioContext.createGain();
        
        osc2.type = 'triangle';
        osc2.frequency.setValueAtTime(200, now);
        osc2.frequency.exponentialRampToValueAtTime(800, now + 1);
        
        gain2.gain.setValueAtTime(0, now);
        gain2.gain.linearRampToValueAtTime(0.15, now + 0.1);
        gain2.gain.exponentialRampToValueAtTime(0.01, now + 1.5);
        
        osc2.connect(gain2);
        gain2.connect(this.sfxGain);
        
        osc2.start(now);
        osc2.stop(now + 1.5);
    }
    
    playProgressSound() {
        const now = this.audioContext.currentTime;
        
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(600, now);
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.1);
        
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        
        osc.connect(gain);
        gain.connect(this.sfxGain);
        
        osc.start(now);
        osc.stop(now + 0.15);
    }
    
    playStageSound() {
        const now = this.audioContext.currentTime;
        
        // Beep corto y agudo
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        osc.type = 'square';
        osc.frequency.setValueAtTime(1200, now);
        
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.08);
        
        osc.connect(gain);
        gain.connect(this.sfxGain);
        
        osc.start(now);
        osc.stop(now + 0.08);
        
        // Segundo beep más grave
        setTimeout(() => {
            const osc2 = this.audioContext.createOscillator();
            const gain2 = this.audioContext.createGain();
            
            osc2.type = 'square';
            osc2.frequency.setValueAtTime(900, this.audioContext.currentTime);
            
            gain2.gain.setValueAtTime(0.1, this.audioContext.currentTime);
            gain2.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.08);
            
            osc2.connect(gain2);
            gain2.connect(this.sfxGain);
            
            osc2.start();
            osc2.stop(this.audioContext.currentTime + 0.08);
        }, 50);
    }
    
    playCompleteSound() {
        const now = this.audioContext.currentTime;
        
        // Acorde ascendente épico
        const frequencies = [261.63, 329.63, 392.00, 523.25];
        
        frequencies.forEach((freq, index) => {
            setTimeout(() => {
                const osc = this.audioContext.createOscillator();
                const gain = this.audioContext.createGain();
                
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, this.audioContext.currentTime);
                
                gain.gain.setValueAtTime(0.2, this.audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.5);
                
                osc.connect(gain);
                gain.connect(this.sfxGain);
                
                osc.start();
                osc.stop(this.audioContext.currentTime + 0.5);
            }, index * 80);
        });
        
        setTimeout(() => {
            this.playWhooshSound();
        }, 400);
    }
    
    playWhooshSound() {
        const now = this.audioContext.currentTime;
        
        const bufferSize = this.audioContext.sampleRate * 0.5;
        const buffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
        const data = buffer.getChannelData(0);
        
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }
        
        const noise = this.audioContext.createBufferSource();
        noise.buffer = buffer;
        
        const filter = this.audioContext.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(2000, now);
        filter.frequency.exponentialRampToValueAtTime(100, now + 0.5);
        filter.Q.value = 1;
        
        const gain = this.audioContext.createGain();
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
        
        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.sfxGain);
        
        noise.start(now);
        noise.stop(now + 0.5);
    }
    
    playGlitchSound() {
        const now = this.audioContext.currentTime;
        
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                const osc = this.audioContext.createOscillator();
                const gain = this.audioContext.createGain();
                
                osc.type = 'square';
                osc.frequency.setValueAtTime(Math.random() * 2000 + 500, this.audioContext.currentTime);
                
                gain.gain.setValueAtTime(0.1, this.audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.05);
                
                osc.connect(gain);
                gain.connect(this.sfxGain);
                
                osc.start();
                osc.stop(this.audioContext.currentTime + 0.05);
            }, i * 30);
        }
    }
    
    playAmbientMusic() {
        const now = this.audioContext.currentTime;
        const duration = 8; // REDUCIDO: Solo 8 segundos (duración del preloader)
        
        const createPad = (freq, detune, delay) => {
            setTimeout(() => {
                const osc = this.audioContext.createOscillator();
                const gain = this.audioContext.createGain();
                
                osc.type = 'sine';
                osc.frequency.value = freq;
                osc.detune.value = detune;
                
                const currentTime = this.audioContext.currentTime;
                gain.gain.setValueAtTime(0, currentTime);
                gain.gain.linearRampToValueAtTime(0.08, currentTime + 1);
                gain.gain.setValueAtTime(0.08, currentTime + duration - 1);
                gain.gain.linearRampToValueAtTime(0, currentTime + duration);
                
                osc.connect(gain);
                gain.connect(this.musicGain);
                
                osc.start(currentTime);
                osc.stop(currentTime + duration);
                
                // NUEVO: Guardar referencia para poder detenerlo
                this.activeOscillators.push({ osc, gain, stopTime: currentTime + duration });
            }, delay);
        };
        
        createPad(130.81, 0, 0);
        createPad(164.81, 5, 500);
        createPad(196.00, -5, 1000);
        createPad(261.63, 10, 1500);
    }
    
    // ============================================
    // CONTROLES
    // ============================================
    
    play(soundName) {
        if (!this.isInitialized || this.isMuted) return;
        
        if (this.sounds[soundName]) {
            try {
                this.sounds[soundName]();
            } catch (error) {
                console.warn('Error playing sound:', error);
            }
        }
    }
    
    // NUEVO: Método para detener todos los sonidos
    stopAll() {
        if (!this.isInitialized) return;
        
        const now = this.audioContext.currentTime;
        
        // Fade out rápido del master gain
        this.masterGain.gain.cancelScheduledValues(now);
        this.masterGain.gain.setValueAtTime(this.masterGain.gain.value, now);
        this.masterGain.gain.linearRampToValueAtTime(0, now + 0.5);
        
        // Detener osciladores activos
        this.activeOscillators.forEach(({ osc, gain, stopTime }) => {
            try {
                if (this.audioContext.currentTime < stopTime) {
                    gain.gain.cancelScheduledValues(now);
                    gain.gain.setValueAtTime(gain.gain.value, now);
                    gain.gain.linearRampToValueAtTime(0, now + 0.5);
                }
            } catch (e) {
                // Oscilador ya detenido
            }
        });
        
        // Limpiar array
        setTimeout(() => {
            this.activeOscillators = [];
        }, 600);
    }
    
    toggleMute() {
        this.isMuted = !this.isMuted;
        this.masterGain.gain.value = this.isMuted ? 0 : this.volumes.master;
        return this.isMuted;
    }
    
    setVolume(type, value) {
        if (type === 'master') {
            this.volumes.master = value;
            this.masterGain.gain.value = value;
        } else if (type === 'music') {
            this.volumes.music = value;
            this.musicGain.gain.value = value;
        } else if (type === 'sfx') {
            this.volumes.sfx = value;
            this.sfxGain.gain.value = value;
        }
    }
}

// Instancia global
window.audioSystem = new AudioSystem();