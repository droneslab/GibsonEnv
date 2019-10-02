with open(osp.join(base_path, "motley_log", 'log.pkl'), 'wb') as fh:
    fh.write(cloudpickle.dumps(env.env.debug_positions))