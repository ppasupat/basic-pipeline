from collections import Counter

import numpy as np

from yournamehere.data.base import Dataset
from yournamehere.utils import batch_iter, PAD, UNK, UNK_INDEX, BOS, EOS


class DemoExample(object):
    """
    A simple text classification example.
    """
    
    def __init__(self, index, sentence, label):
        self.index = index
        self.sentence = sentence
        self.label = label or None

    def preprocess(self, config):
        """
        Happens before metadata is populated.
        """
        self.tokens = self.sentence.split()
        if config.data.get_('lower'):
            self.tokens = [x.lower() for x in self.tokens]

    def postprocess(self, config, meta):
        """
        Happens after metadata is populated.
        """
        self.token_indices = [meta.vocab_x.get(x, UNK_INDEX) for x in self.tokens]
        if self.label:
            self.label_index = meta.labels_x[self.label]
        else:
            self.label_index = None

    def __str__(self):
        return 'Example({} -> {})'.format(' '.join(self.tokens), self.label)

    __repr__ = __str__

    @property
    def length(self):
        return len(self.tokens)


class DemoDataset(Dataset):
    """
    A simple text classification dataset.
    """

    def __init__(self, config, meta):
        super().__init__(config, meta)
        self._data = {}
        self._iters = {}
        for name in config.data.files:
            self._data[name] = self._read_data(config.data.files[name])
            print('Read {} {} examples'.format(len(self._data[name]), name))
        for name in self._data:
            for example in self._data[name]:
                example.preprocess(config)
        if not hasattr(meta, 'vocab'):
            # Note: meta.vocab is already there if the model was loaded
            #   from a snapshot.
            self._gen_vocab(self._data['train'], config, meta)
        for name in self._data:
            for example in self._data[name]:
                example.postprocess(config, meta)

    def _read_data(self, filename):
        examples = []
        with open(filename) as fin:
            for index, line in enumerate(fin):
                label, sentence = line.rstrip('\n').split('\t')
                example = DemoExample(index, sentence, label)
                examples.append(example)
        return examples

    def _gen_vocab(self, examples, config, meta):
        # Gather the tokens and labels
        # Note: ..._x means reverse lookup
        meta.vocab_cnt = Counter()
        meta.labels_cnt = Counter()
        for example in examples:
            for x in example.tokens:
                meta.vocab_cnt[x] += 1
            assert example.label is not None
            meta.labels_cnt[example.label] += 1
        # Finalize
        meta.vocab_cnt = dict(meta.vocab_cnt)
        meta.labels_cnt = dict(meta.labels_cnt)
        if 'min_freq' in config.data:
            meta.vocab_cnt = {
                x: v for (x, v) in meta.vocab_cnt.items()
                if v >= config.data.min_freq
            }
        meta.vocab = [PAD, UNK, BOS, EOS] + sorted(meta.vocab_cnt)
        meta.vocab_x = {x: i for (i, x) in enumerate(meta.vocab)}
        meta.labels = sorted(meta.labels_cnt)
        meta.labels_x = {x: i for (i, x) in enumerate(meta.labels)}

    def init_iter(self, name):
        """
        Initialize the iterator for the specified data split.
        """
        data = self._data[name][:]
        if name == 'train':
            np.random.shuffle(data)
        self._iters[name] = batch_iter(
            data, self.batch_size, (lambda x: -x.length)
        )

    def get_iter(self, name):
        """
        Get the iterator over the specified data split.
        """
        return self._iters[name]

    def evaluate(self, batch, logit, prediction, stats, fout=None):
        """
        Evaluate the predictions and write the results to stats.

        Args:
            batch: list[Example]
            prediction: Tuple[Tensor, Tensor]
                First Tensor: (batch,)
                    predicted label indices.
                Second Tensor: (batch, num_labels)
                    prediction score for each label.
            stats: Stats
        """
        pred_label_indices, pred_scores = prediction
        ordered = sorted(
            zip(batch, pred_label_indices, pred_scores),
            key=lambda x: x[0].index
        )
        for example, pred_label_index, pred_score in ordered:
            pred_label_index = pred_label_index.item()
            if fout:
                print(pred_label_index, file=fout)
            if example.label_index == pred_label_index:
                stats.accuracy += 1
