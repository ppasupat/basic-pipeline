def create_dataset(config, meta):
    if config.data.name == 'demo':
        from yournamehere.data.demo import DemoDataset
        return DemoDataset(config, meta)
    raise ValueError('Unknown data name: {}'.format(config.data.name))
