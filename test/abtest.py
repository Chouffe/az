import utils
import api


def objective_function(a1, a2, **kwargs):
    return 5 * a1 + 10 * a2 - 2*a1 * a2 + utils.noise()


def format_results(ab, az):
    header = "%s | %s | %s " % ("", "AB/Testing", "AZ/Testing")
    score = "%s | %.1f | %.1f " % ("Best Score",
                                   ab._current_best_score,
                                   az._current_best_score)
    point = "%s | %s | %s " % ("Best Point",
                               ab._current_best_point,
                               az._current_best_point)
    return "%s\n%s\n%s\n" % (header, score, point)


def run_test(objective_function, features, T=100):
    ab = api.ABTesting()
    az = api.AZTesting()

    for feature_name in features:
        ab.add_feature(feature_name, "binary")
        az.add_feature(feature_name, "binary")

    # AB/Testing
    for _ in range(T):
        point_to_try = ab.get_candidate()
        score = objective_function(**point_to_try)
        ab.save_result(point_to_try, score)

    # AZ/Testing
    for _ in range(T):
        point_to_try = az.get_candidate()
        score = objective_function(**point_to_try)
        az.save_result(point_to_try, score)
        # TODO: handle that with a queue server side
        time.sleep(.2)

    return format_results(ab, az)


print run_test(objective_function, ['a' + str(n) for n in range(1, 30)], T=10)
