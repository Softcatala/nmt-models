import tensorflow as tf
import opennmt as onmt
class Softcatala(onmt.models.Transformer):
    """Defines a base Transformer model using relative position representations as
    described in https://arxiv.org/abs/1803.02155.
    """

    def __init__(self):
        super().__init__(position_encoder_class=None, maximum_relative_position=20, share_embeddings=sequence_to_sequence.EmbeddingsSharingLevel.AUTO)
