-----WORK IN PROGRESS-----

The synthesizer sequencer currently generates sine or square waves real-time or within a sequence.
To initiate a sequence, play the notes you would like included, select a wave type, then hit the 
"PLAY" button.

The synthesizer uses multithreading in order to allow simultaneous playback while the user configures
elements of the GUI. Eventually, this will include modulation controls, more wave types, etc.

It is programmed in Python, heavily utilizing the numpy, pygame, scipy, and PyQt modules.

----------TO-DO-----------

Re-work waveform generation using linspace method for a uniform, consistent amplitude acrosswave types.

Add modulation controls to the GUI.

Add triangle and sawtooth waves.

Implement more threads for the addition of layered wave generation.