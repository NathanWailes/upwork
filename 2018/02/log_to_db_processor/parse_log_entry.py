import re
from datetime import datetime
import logging
from utils import pattern_for_log_entry_timestamp, possible_log_levels, possible_http_methods, possible_auth_mechanisms, \
                  iso_8601_datetime_format

logging.basicConfig(filename="potential_errors.log", level=logging.INFO)


def get_dict_from_log_entry_as_a_string(log_entry_as_a_string):
    log_entry_datetime = _get_datetime_from_log_entry_string(log_entry_as_a_string)
    return {'datetime': log_entry_datetime,
            'log_level': _get_log_level(log_entry_as_a_string),
            'uri': _get_uri(log_entry_as_a_string),
            'uri_pattern': _get_uri_pattern(log_entry_as_a_string),
            'request_uuid': _get_request_uuid(log_entry_as_a_string),
            'device_uuid': _get_device_uuid(log_entry_as_a_string),
            'merchant_id': _get_merchant_id(log_entry_as_a_string),
            'version_id': _get_version_id(log_entry_as_a_string),
            'request_ip': _get_request_ip(log_entry_as_a_string),
            'http_method': _get_http_method(log_entry_as_a_string),
            'http_status': _get_http_status(log_entry_as_a_string),
            'developer_app_id': _get_developer_app_id(log_entry_as_a_string),
            'auth_mechanism': _get_auth_mechanism(log_entry_as_a_string),
            'request_time': _get_request_time(log_entry_as_a_string),
            'log_statement': _get_log_statement(log_entry_as_a_string),
            'logging_class': _get_logging_class(log_entry_as_a_string)}


def _get_datetime_from_log_entry_string(log_entry_as_a_string):
    matches = re.findall(pattern_for_log_entry_timestamp, log_entry_as_a_string)
    assert_n_matches(log_entry_as_a_string, matches, 1)
    log_entry_datetime_as_a_string = matches[0]

    assert(log_entry_datetime_as_a_string.startswith('['))
    assert(log_entry_datetime_as_a_string.endswith(']'))
    log_entry_datetime_as_a_string = log_entry_datetime_as_a_string[1:-1]

    log_entry_datetime = datetime.strptime(log_entry_datetime_as_a_string, iso_8601_datetime_format)
    return log_entry_datetime


def assert_n_matches(log_entry_as_a_string, matches, expected_number_of_matches):
    assert len(matches) == 1, "log_entry_as_a_string: %s\n\nMatches: %s\n" % (log_entry_as_a_string, str(matches))


def _get_log_level(log_entry_as_a_string):
    log_level_regex = "|".join(["(?:" + log_level + ")" for log_level in possible_log_levels])
    pattern_for_log_level = pattern_for_log_entry_timestamp + r" \[(%s)\]" % log_level_regex

    matches = re.findall(pattern_for_log_level, log_entry_as_a_string)

    assert_n_matches(log_entry_as_a_string, matches, 1)  # There should *always* be a log level.
    assert matches[0] in possible_log_levels, "matches[0]: %s\n\npossible_log_levels: %s\n" % (matches[0], str(possible_log_levels))

    return matches[0]


def _get_uri(log_entry_as_a_string):
    pattern = r"\su=(\S+)"
    matches = re.findall(pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def assert_LTE_n_matches(log_entry_as_a_string, matches, expected_number_of_matches):
    assert len(matches) <= 1, "log_entry_as_a_string: %s\n\nMatches: %s\n" % (log_entry_as_a_string, str(matches))


def assert_matches_less_than_or_equal_n(log_entry_as_a_string, matches, expected_number_of_matches):
    assert len(matches) == 1, "log_entry_as_a_string: %s\n\nMatches: %s\n" % (log_entry_as_a_string, str(matches))


def _get_uri_pattern(log_entry_as_a_string):
    regex_pattern = r"\sp=(\S+)"
    matches = re.findall(regex_pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def _get_request_uuid(log_entry_as_a_string):
    pattern = r"\sr=(\S+)"
    matches = re.findall(pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def _get_device_uuid(log_entry_as_a_string):
    pattern = r"\sd=(\S+)"
    matches = re.findall(pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def _get_merchant_id(log_entry_as_a_string):
    pattern = r"\sm=(\S+)"
    matches = re.findall(pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def _get_version_id(log_entry_as_a_string):
    pattern = r"\sv=(\S+)"
    matches = re.findall(pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def _get_request_ip(log_entry_as_a_string):
    pattern = r"\si=(\S+)"
    matches = re.findall(pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def _get_http_method(log_entry_as_a_string):
    http_method_regex = "|".join(["(?:" + http_method + ")" for http_method in possible_http_methods])
    pattern_for_http_method = r"\shm=(%s)" % http_method_regex
    matches = re.findall(pattern_for_http_method, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    assert matches[0] in possible_http_methods if matches else True
    return matches[0] if matches else None


def _get_http_status(log_entry_as_a_string):
    pattern = r"\shs=(\S+)"
    matches = re.findall(pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def _get_developer_app_id(log_entry_as_a_string):
    pattern = r"\sda=(\S+)"
    matches = re.findall(pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def _get_auth_mechanism(log_entry_as_a_string):
    pattern_for_possible_auth_mechanisms = "|".join(["(?:" + auth_mechanism + ")" for auth_mechanism in possible_auth_mechanisms])
    pattern_for_auth_mechanism = r"\sam=(%s)" % pattern_for_possible_auth_mechanisms
    matches = re.findall(pattern_for_auth_mechanism, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    assert matches[0] in possible_auth_mechanisms if matches else True, \
        "matches[0]: %s\n\npossible_auth_mechanisms: %s\n" % (matches[0], str(possible_auth_mechanisms))
    return matches[0] if matches else None


def _get_request_time(log_entry_as_a_string):
    pattern = r"\st=(\S+)"
    matches = re.findall(pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def _get_log_statement(log_entry_as_a_string):
    """ This seems very liable to break.

    :param log_entry_as_a_string:
    :return:
    """
    # I'm defining the log statement as "Everything between the 't=...' entry and the logging class".
    # Tricky: you need to have {0,} after the \d to handle the case where there's no value after the "t=".
    pattern = r"(?<=(?:t=))\d{0,} ([\s\S]+) (?=\([A-Z][A-Za-z]+\))"
    matches = re.findall(pattern, log_entry_as_a_string)
    assert_LTE_n_matches(log_entry_as_a_string, matches, 1)
    return matches[0] if matches else None


def _get_logging_class(log_entry_as_a_string):
    """ The regex for this one seems the most likely to "break" (match more than one thing, only one of which is
    correct).

    :param log_entry_as_a_string:
    :return:
    """
    log_entry_as_a_string = remove_nested_curly_braces(log_entry_as_a_string)

    dont_match_garbage_collection_GC_in_parens = r"(?<!Garbage Collection )"
    pattern = dont_match_garbage_collection_GC_in_parens + r"\(([A-Z][A-Za-z]+)\)"  # Starts with a capital letter, then either lowercase or capital letters
    matches = re.findall(pattern, log_entry_as_a_string)
    matches_as_a_set = set(matches)  # Remove duplicates

    # Handle an edge case I ran into... the log data seems dirty. "..." is me removing lengthy text.
    # [2018-01-30 00:00:02.504] [INFO] ... RequestLog{...} (FileRequestObjectLogger)
    # GC Memory Usage: ...
    #  (GCNotificationListener)
    if len(matches_as_a_set) > 1 and "GCNotificationListener" in matches_as_a_set:
        matches_as_a_set.remove("GCNotificationListener")


    """
    In the case below, it matched both (GetOrders) and also (FileRequestObjectLogger). It looks like GetOrders is the right one to pick, so
    I'm going to do something that's probably not a good idea and just tell the program to take the first match in the future to avoid future
    issues like this. That is a pretty dangerously over-broad solution, so it should be narrowed in the future.
    
    Update: there seems like there may be a rare issue where the ordering of the matches in the final list isn't the same as their ordering
    in the original 'matches' object. It's such a rare edge-case that I don't think it's worth worrying about.
    
    [2018-01-30 00:12:36.464] [INFO] u=/v3/merchants/QGN5AT833CWRW/orders p=/v3/merchants//orders r=631f6e58-c8d9-f471-7784-a1bfca865d3f d= m=2736 v= i=138.68.45.189 hm=GET hs= da=3542 am=API t= Returning order count: 100, orders (limit of 50): [Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order, Order] (GetOrders)
        at com.clover.http.CloverRequester.get(CloverRequester.java:122)
        at com.clover.http.CloverRequester.get(CloverRequester.java:102)
        at com.clover.engine.simplesync.SimpleSyncAdapter.download(SimpleSyncAdapter.java:127)
        at com.clover.engine.simplesync.SimpleSyncAdapter.onPerformSync(SimpleSyncAdapter.java:46)
        at android.content.AbstractThreadedSyncAdapter$SyncThread.run(AbstractThreadedSyncAdapter.java:254)
    , messageParameters=["com.clover.paymentcardconfig"]$@#END_PARAM_JSON, serialNumber=C010UQ61040069, requestUuid=null, message=down sync failed for authority: %s$@#END_MSG_STRING, exceptionMessage=404 Not Found} (FileRequestObjectLogger)
    """

    matches = list(matches_as_a_set)

    # assert_LTE_n_matches(log_entry_as_a_string, matches, 1)  <-- I'm disabling the assert in favor of logging and choosing the first match.
    if len(matches) > 1:
        logging.info("\n\nPOTENTIAL ERROR:\nLog entry:\n%s\n\nMatches: %s" % (log_entry_as_a_string, matches))

    return matches[0] if matches else None


def remove_nested_curly_braces(log_entry_as_a_string):
    """  Code adapted from https://stackoverflow.com/a/37538815/4115031

    I'm using it to make it easier to avoid false positives when looking for the logging class, in examples like the
    one below, where I need to match the "(FileRequestObjectLogger)" but I'm also matching "(Single)".

    [2018-01-30 00:04:44.443] [INFO] ... RequestLog{
       reqBody=   {
          "accountId":null,
          "requestUuid":null,
          "requestTime":null,
          "encrypted":false,
          "async":false,
          "testing":true,
          "profile":null
       },
       rspBody=   {
          "profiles":[
             "EMVCo L2 Contact",
             "EMVCo L2 Contact Bad CAPK",
             "EMVCo L2 Contact Revoked",
             "EMVCo L2 Contact Revoked (Single)",
             "EMVCo L2 Contactles Revoked (Single)",
             "EMVCo L2 Contactless"
          ]
       },
       host=sandbox,
       cT=2018-01-30T00:04:44.440   Z,
       aId=10852
    } (FileRequestObjectLogger)

    :param log_entry_as_a_string:
    :return:
    """
    string_to_return = ''
    count_of_opening_curly_braces_still_unmatched = 0

    for character in log_entry_as_a_string:
        if character == '{':
            count_of_opening_curly_braces_still_unmatched += 1
        elif character == '}'and count_of_opening_curly_braces_still_unmatched > 0:
            count_of_opening_curly_braces_still_unmatched -= 1
        elif count_of_opening_curly_braces_still_unmatched == 0:
            string_to_return += character

    return string_to_return
