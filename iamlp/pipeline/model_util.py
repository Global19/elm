import copy

from iamlp.model_selectors.util import get_args_kwargs_defaults

PARTIAL_FIT_MODELS = [
    # Classification
    'sklearn.naive_bayes:MultinomialNB',
    'sklearn.naive_bayes:BernoulliNB',
    'sklearn.linear_model:Perceptron',
    'sklearn.linear_model:SGDClassifier',
    'sklearn.linear_model:PassiveAggressiveClassifier',
    # Regression
    'sklearn.linear_model:SGDRegressor',
    'sklearn.linear_model:PassiveAggressiveRegressor',
    # Clustering
    'sklearn.cluster:MiniBatchKMeans',
    # Decomposition
    'sklearn.decomposition:MiniBatchDictionaryLearning',
    'sklearn.decomposition:IncrementalPCA',
    'sklearn.cluster:MiniBatchKMeans',
]


def final_on_sample_step(fitter, model, sample,
                         iter_offset,
                         fit_kwargs,
                         selector_dict,
                         get_y_func=None,
                         get_y_kwargs=None,
                         get_weight_func=None,
                         get_weight_kwargs=None,
                      ):
    if not hasattr(model, fit_func):
        raise IAMLPConfigError('Model {} has no method {}'.format(model, fit_func))
    fitter = getattr(model, fit_func)
    args, kwargs = get_args_kwargs_defaults(fitter)
    fit_kwargs = fit_kwargs or {}
    fit_kwargs = copy.deepcopy(fit_kwargs)
    if 'classes' in kwargs:
        if classes is None:
            raise IAMLPConfigError('Expected "classes" '
                                   'in fit_kwargs to be a list of all '
                                   'possible classes.  Got {}'.format(classes))
        fit_kwargs['classes'] = classes
    if 'iter_offset' in kwargs:
        fit_kwargs['iter_offset'] = iter_offset
    if 'check_input' in kwargs:
        fit_kwargs['check_input'] = True
    if 'sample_weight' in kwargs and get_weight_func is not None:
        get_weight_kwargs = get_weight_kwargs or {}
        fit_kwargs['sample_weight'] = get_weight_func(sample, **get_weight_kwargs)
    if any(a.lower() == 'y' for a in args):
        y = get_y_func(sample)
        fit_args = (sample.values, y)
    else:
        fit_args = (sample.values, )
    return fit_args, fit_kwargs