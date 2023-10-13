import tensorflow as tf
import opennmt as onmt
class SoftcatalaModel(onmt.models.Transformer):
    """Defines a base Transformer model using relative position representations as
    described in https://arxiv.org/abs/1803.02155.
    """

    def __init__(self):
        super().__init__(share_embeddings=onmt.models.sequence_to_sequence.EmbeddingsSharingLevel.AUTO)
        
model = SoftcatalaModel

# TransformerRelative: *** model cfg: num_units: 512, num_heads: 8, ffn_inner_dim: 2048, maximum_relative_position: 20
#
#          num_units: The number of hidden units.
#          num_heads: The number of heads in each self-attention layers.
#          ffn_inner_dim: The inner dimension of the feed forward layers.
#          maximum_relative_position: Maximum relative position representation
#          Where the input / output dimensions are much greater than the hidden input dimension. 

