from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from magenta.music import midi_io

# Load the model bundle
bundle_path = '/path/to/attention_rnn.mag'
bundle = sequence_generator_bundle.read_bundle_file(bundle_path)
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['attention_rnn']

def generate_melody(model, num_steps=64, temperature=1.0):
    # Initialize an empty sequence
    primer_sequence = model.generate_primer_sequence(num_steps=num_steps)
    # Generate the melody
    melody, _ = model.generate(primer_sequence, temperature=temperature)
    return melody


def save_melody_to_midi(melody, output_path):
    # Create a NoteSequence from the generated melody
    note_sequence = melody.to_sequence()

    # Save as a MIDI file
    midi_io.note_sequence_to_midi_file(note_sequence, output_path)
