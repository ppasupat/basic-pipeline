def create_model(config, meta):
    if config.model.name == 'demo':
        from yournamehere.model.demo import DemoModel
        return DemoModel(config, meta)
    raise ValueError('Unknown model name: {}'.format(config.model.name))
