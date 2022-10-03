import tensorflow as tf
import opennmt as onmt
class Softcatala(onmt.models.Transformer):
    """Defines a base Transformer model using relative position representations as
    described in https://arxiv.org/abs/1803.02155.
    """

    def __init__(self):
        super().__init__(
            num_units=1024,
            num_heads=16,
            ffn_inner_dim=4096,
            position_encoder_class=None,
            maximum_relative_position=20,
            share_embeddings=sequence_to_sequence.EmbeddingsSharingLevel.AUTO
        )
        
#          num_units: The number of hidden units.
#          num_heads: The number of heads in each self-attention layers.
#          ffn_inner_dim: The inner dimension of the feed forward layers.
#          maximum_relative_position: Maximum relative position representation
 
