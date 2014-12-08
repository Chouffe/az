import objective_functions
import experiments_az
import experiments_ab


# Landing Page Experiment
landing_page = {
    'uuid': 'demo1',
    'schema_uuid': 'lp',
    'objective_function': objective_functions.obj_function_landing_page,
    'objective_function_draw':
    objective_functions.obj_function_landing_page_draw,
    'n_trials': 200,
    'n_points': 100,
    'az': True,
    'ab': True,
    'feature_names': [
        "background",
        "font_size",
        "color",
        "number_columns",
        "popup"
    ],
    'feature_distributions': [
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "binary"
    ],
    'feature_params': [
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 15},
        {'low': 0, 'high': 6},
        {'low': 0, 'high': 10},
        {}
    ]
}

landing_page2 = {
    'uuid': 'demo2',
    'schema_uuid': 'lp2',
    'objective_function': objective_functions.obj_function_landing_page,
    'objective_function_draw':
    objective_functions.obj_function_landing_page_draw,
    'n_trials': 200,
    'n_points': 100,
    'az': True,
    'ab': True,
    'feature_names': [
        "background",
        "font_size",
        "color",
        "number_columns",
        "popup",

        "useless_background",
        "useless_button",
        "useless_form",
        "useless_color",
        "useless_text",
        "useless_link",
        "useless_column",
        "useless_layout",
        "useless_popup"
    ],
    'feature_distributions': [
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "binary",

        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "uniform_discrete",
        "binary"
    ],
    'feature_params': [
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 15},
        {'low': 0, 'high': 6},
        {'low': 0, 'high': 10},
        {},

        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {}
    ]
}

# Landing Page Experiment
black_box = {
    'uuid': 'demo3',
    'schema_uuid': 'blackbox',
    'objective_function': objective_functions.obj_function_black_box1,
    'objective_function_draw': objective_functions.obj_function_black_box1,
    'n_trials': 50,
    'n_points': 300,
    'az': True,
    'ab': False,
    'feature_names': [
        "a1",
        "a2",

        "useless_a3",
        "useless_a4",
        "useless_a5",
        "useless_a6",
        "useless_a7",
        "useless_a8",
        "useless_a9"
    ],
    'feature_distributions': [
        "uniform",
        "uniform",

        "uniform",
        "uniform",
        "uniform",
        "uniform",
        "uniform",
        "uniform",
        "uniform"
    ],
    'feature_params': [
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},

        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10},
        {'low': 0, 'high': 10}
    ]
}


def get_experiment(uuid):
    experiments = [landing_page, landing_page2, black_box]
    for exp in experiments:
        if exp['uuid'] == uuid:
            return exp
    return None


def get_experiment_by_schema_uuid(schema_uuid):
    experiments = [landing_page, landing_page2, black_box]
    for exp in experiments:
        if exp['schema_uuid'] == schema_uuid:
            return exp
    return None


def run(data, f):
    """Runs f with data -  Return f(data)"""

    assert 'uuid' in data, "uuid not in data"
    assert 'schema_uuid' in data, "schema_uuid not in data"
    assert 'objective_function_draw' in data, \
           "objective_function_draw not in data"
    assert 'n_points' in data, "n_points not in data"
    assert 'n_trials' in data, "n_trials not in data"
    assert 'feature_names' in data, "feature_names not in data"
    assert 'feature_distributions' in data, "feature_distributions not in data"
    assert 'feature_params' in data, "feature_params not in data"

    return f(data['objective_function_draw'],
             data['n_points'],
             data['n_trials'],
             len(data['feature_names']),
             uuid=data['schema_uuid'],
             feature_names=data['feature_names'],
             feature_distributions=data['feature_distributions'],
             feature_params=data['feature_params'])


def run_demo(uuid):
    experiment = get_experiment(uuid)
    if experiment is None:
        return None
    else:
        if experiment['az']:
            run(experiment, experiments_az.run_experiment)
        if experiment['ab']:
            run(experiment, experiments_ab.run_experiment)
