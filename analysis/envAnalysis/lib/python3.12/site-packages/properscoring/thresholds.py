

@guvectorize(["void(float64[:], float64[:], float64[:], float64[:])"],
             "(),(n),(m)->(m)", nopython=True)
def _threshold_decomp_gufunc(observation, forecasts, thresholds, result):
    # both forecasts and thresholds are assumed sorted in NumPy's sort order
    obs = observation[0]
    if np.isnan(obs):
        result[:] = np.nan
        return

    n_thresholds = len(thresholds)
    n_forecasts = len(forecasts)
    while np.isnan(forecasts[n_forecasts - 1]) and n_forecasts > 0:
        n_forecasts -= 1

    inv_n_forecasts = 1.0 / n_forecasts

    i = 0
    j = 0
    while i < n_forecasts and j < n_thresholds:
        forecast = forecasts[i]
        threshold = thresholds[j]

        if forecast < threshold:
            i += 1
        else:
            probability = i * inv_n_forecasts
            binary_obs = obs < threshold
            result[j] = (probability - binary_obs) ** 2
            j += 1

    for k in range(j, n_thresholds):
        threshold = thresholds[k]
        binary_obs = obs < threshold
        # probability is always 1, so we can skip the square
        result[k] = 1 - binary_obs


def threshold_decomposition(observations, forecasts, thresholds,
                            issorted=False, axis=-1):
    """
    Threshold decomposition of the continuous ranked probability score (CRPS)

    This function calculates the Brier score for exceedance at each given
    threshold (the values z in the equation below). The resulting Brier scores
    can thus be summed along the last axis to calculate CRPS, as

    .. math::
        CRPS(F, x) = \int_z BS(F(z), H(z - x)) dz

    where $F(x) = \int_{z \leq x} p(z) dz$ is the cumulative distribution
    function (CDF) of the forecast distribution $F$, $x$ is a point estimate of
    the true observation (observational error is neglected), $BS$ denotes the
    Brier score and $H(x)$ denotes the Heaviside step function, which we define
    here as equal to 1 for x >= 0 and 0 otherwise.

    It is more efficient to calculate CRPS directly, but this threshold
    decomposition itself provides a useful summary of model quality as a
    function of measurement values.

    Parameters
    ----------
    observations : float or np.ndarray
        Observations float or array. Missing values (NaN) are given scores of
        NaN.
    forecasts : float or np.ndarray
        Array of forecasts ensemble members, of the same shape as observations
        except for the axis along which the threshold decomposition is
        calculated (which should be the axis corresponding to the ensemble). If
        forecasts has the same shape as observations, the forecasts are treated
        as deterministic. Missing values (NaN) are ignored.
    thresholds : array_like
        Threshold values at which to calculate the exceedence Brier score which
        contributes to CRPS.
    issorted : bool, optional
        Optimization flag to indicate that the elements of `ensemble` are
        already sorted along `axis`.
    axis : int, optional
        Axis in forecasts which corresponds to different ensemble members,
        along which to calculate the threshold decomposition.

    Returns
    -------
    out : np.ndarray
        Threshold decomposition for each ensemble forecast against the
        observations. The threshold decomposition will have the same shape as
        observations, except for an additional final dimension, which
        corresponds to the different threshold values.

    References
    ----------
    Gneiting, T. and Ranjan, R. Comparing density forecasts using threshold-
       and quantile-weighted scoring rules. J. Bus. Econ. Stat. 29, 411-422
       (2011). http://www.stat.washington.edu/research/reports/2008/tr533.pdf

    See also
    --------
    crps, brier_score
    """
    observations = np.asarray(observations)
    thresholds = np.asarray(thresholds)
    forecasts = np.asarray(forecasts)

    if forecasts.ndim:
        if axis < 0:
            axis += forecasts.ndim
        order = [n for n in range(forecasts.ndim) if n != axis] + [axis]
        forecasts = np.transpose(forecasts, order)

    if forecasts.shape == observations.shape:
        forecasts = forecasts[..., np.newaxis]

    if observations.shape != forecasts.shape[:-1]:
        raise ValueError('observations and forecasts must have matching '
                         'shapes or matching shapes except along `axis=%s`'
                         % axis)

    if thresholds.ndim > 1 or not (np.sort(thresholds) == thresholds).all():
        raise ValueError('thresholds must be 1D and sorted')
    thresholds = thresholds.reshape((1,) * observations.ndim + (-1,))

    if not issorted:
        forecasts = np.sort(forecasts, axis=-1)

    return _threshold_decomp_gufunc(observations, forecasts, thresholds)


def threshold_decomposition_slow(observations, forecasts, thresholds, axis=-1):
    observations = np.asarray(observations)
    thresholds = np.asarray(thresholds)
    forecasts = np.asarray(forecasts)

    def threshold_exceedances(x):
        # NaN safe calculation of threshold exceedances
        # TODO: expose a version of this function in the public API?
        # add an extra dimension to `x` and broadcast `thresholds` so that it
        # varies along that new dimension
        with warnings.catch_warnings():
            warnings.filterwarnings(
                'ignore', 'invalid value encountered in greater')
            exceeds = (x[..., np.newaxis] >
                       thresholds.reshape(*([1] * x.ndim + [-1]))
                       ).astype(float)
        if x.ndim == 0 and np.isnan(x):
            exceeds[:] = np.nan
        else:
            exceeds[np.where(np.isnan(x))] = np.nan
        return exceeds

    binary_obs = threshold_exceedances(observations)
    if observations.shape == forecasts.shape:
        prob_forecast = threshold_exceedances(forecasts)
    elif (observations.shape ==
          tuple(s for n, s in enumerate(forecasts.shape)
                if n != axis % forecasts.ndim)):
        forecasts = np.swapaxes(forecasts, axis, -1)
        # axis=-2 should be the 'realization' axis, after swapping that axes
        # to the end of forecasts and inserting one extra axis
        prob_forecast = np.nanmean(threshold_exceedances(forecasts), axis=-2)
    else:
        raise ValueError('observations and forecasts must have matching '
                         'shapes or matching shapes except along `axis=%s`'
                         % axis)
    return brier_score(binary_obs, prob_forecast)