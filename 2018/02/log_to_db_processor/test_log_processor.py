import filecmp
import unittest

import os

from datetime import datetime

from log_processor import _get_log_entries_as_strings
from parse_log_entry import get_dict_from_log_entry_as_a_string
from utils import possible_log_levels, possible_http_methods, possible_auth_mechanisms, remove_file

base_path = './'
test_log_path = base_path + 'unittest_log.log'
test_log_offset_file_path = test_log_path + ".offset"


def save_setup_files(test_log_string):
    save_string_to_file(test_log_string, path=test_log_path)


def save_string_to_file(string_to_save, path):
    with open(path, 'w') as outfile:
        outfile.write(string_to_save)


class TestParseLogFileIntoLogEntries(unittest.TestCase):

    def setUp(self):
        self.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        for file_path in [test_log_path, test_log_offset_file_path]:
            if os.path.isfile(file_path):
                remove_file(file_path)

    def test_empty_log_file(self):
        log_data = ""
        save_setup_files(log_data)

        log_entries_as_strings = _get_log_entries_as_strings(test_log_path)

        log_entries = [log_entry for log_entry in log_entries_as_strings]
        self.assertEqual([], log_entries)

    def test_single_existing_log_entry(self):
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm= hs= da= am= t= RolloutJob started (RolloutJob)\n"
        save_setup_files(log_data)

        log_entries_as_strings = _get_log_entries_as_strings(test_log_path)

        self.assertEqual(log_data, next(log_entries_as_strings))

    def test_two_existing_log_entries(self):
        entry_one = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm= hs= da= am= t= RolloutJob started (RolloutJob)\n"
        entry_two = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm= hs= da= am= t= Found 0 rollout(s) to process: [] (RolloutJob)\n"
        log_data = entry_one + entry_two
        save_setup_files(log_data)

        log_entries_as_strings = _get_log_entries_as_strings(test_log_path)
        self.assertEqual(entry_one, next(log_entries_as_strings))
        self.assertEqual(entry_two, next(log_entries_as_strings))

    def test_a_single_existing_garbage_collection_log_entry(self):
        log_data = ("[2018-01-30 00:00:00.325] [INFO] u= p= r= d= m= v= i= hm= hs= da= am= t= Garbage Collection (GC) event. gcAction=end of minor GC, gcName=ParNew, gcCause=Allocation Failure, gcThreadCount=5.\n"
                     "GC Memory Usage: poolName=Par Survivor Space, init=22282240, max=44630016, committedBefore=22282240, committedAfter=22282240, usedBefore=19330160, usedAfter=19355248\n"
                     "GC Memory Usage: poolName=Code Cache, init=2555904, max=251658240, committedBefore=74514432, committedAfter=74514432, usedBefore=73897472, usedAfter=73897472\n"
                     "GC Memory Usage: poolName=Compressed Class Space, init=0, max=1073741824, committedBefore=14475264, committedAfter=14475264, usedBefore=13641704, usedAfter=13641704\n"
                     "GC Memory Usage: poolName=Metaspace, init=0, max=188743680, committedBefore=111390720, committedAfter=111390720, usedBefore=106635656, usedAfter=106635656\n"
                     "GC Memory Usage: poolName=Par Eden Space, init=178782208, max=357433344, committedBefore=178782208, committedAfter=178782208, usedBefore=178782208, usedAfter=0\n"
                     "GC Memory Usage: poolName=CMS Old Gen, init=112197632, max=895483904, committedBefore=614846464, committedAfter=614846464, usedBefore=357923104, usedAfter=359790496\n"
                     "(GCNotificationListener)\n")
        save_setup_files(log_data)

        log_entries_as_strings = _get_log_entries_as_strings(test_log_path)
        self.assertEqual(log_data, next(log_entries_as_strings))

    def test_a_single_existing_error_log_entry(self):
        log_data = ("[2018-01-30 00:18:20.989] [ERROR] u=/cos/v1/pay p=/cos/v1/pay r=c44ac4ff-6ab7-61fc-fb69-1e32c368ad68 d=C91F3A3F486DBAD70D9838184B8FE51F m=5351 v=1591650 i=24.120.168.194 hm=POST hs= da= am=APP t= Error executing runnable for task Record transaction info (CloverRunnable)\n"
                    "com.clover.serverkit.domain.DomainException: Error creating payment extra\n"
                    "	at com.clover.server.controller.ExtraController.createOrUpdateExtra(ExtraController.java:188)\n"
                    "	at com.clover.server.controller.ExtraController$3.tx(ExtraController.java:136)\n"
                    "	at com.clover.serverkit.persistence.db.VoidTransactable.transact(VoidTransactable.java:8)\n"
                    "	at com.clover.serverkit.persistence.db.VoidTransactable.transact(VoidTransactable.java:5)\n"
                    "	at com.clover.serverkit.persistence.db.DatabaseBase.transact(DatabaseBase.java:105)\n"
                    "	at com.clover.serverkit.persistence.db.DatabaseTransactor.transact(DatabaseTransactor.java:109)\n"
                    "	at com.clover.server.controller.ExtraController.createOrUpdateExtra(ExtraController.java:133)\n"
                    "	at com.clover.server.controller.BasePaymentController.createOrUpdatePaymentExtra(BasePaymentController.java:2405)\n"
                    "	at com.clover.server.handlers.api.v1.order.PayHandler$2.doRun(PayHandler.java:363)\n"
                    "	at com.clover.serverkit.CloverRunnable.run(CloverRunnable.java:35)\n"
                    "	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)\n"
                    "	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)\n"
                    "	at java.lang.Thread.run(Thread.java:745)\n"
                    "Caused by: com.clover.serverkit.persistence.db.DbException: An error occurred while attempting to access the database.\n"
                    "	at com.clover.serverkit.persistence.db.DbException.causedBy(DbException.java:70)\n"
                    "	at com.clover.serverkit.persistence.db.DatabaseExecute.run(DatabaseExecute.java:44)\n"
                    "	at com.clover.serverkit.persistence.db.Databases.doUpdate(Databases.java:361)\n"
                    "	at com.clover.serverkit.persistence.db.Databases.insertWithoutValues(Databases.java:277)\n"
                    "	at com.clover.serverkit.persistence.db.Databases.upsert(Databases.java:299)\n"
                    "	at com.clover.server.controller.ExtraController.createOrUpdateExtra(ExtraController.java:182)\n"
                    "	... 12 more\n"
                    "Caused by: java.sql.SQLException: Data truncated for column 'type' at row 1\n"
                    "	at com.mysql.jdbc.SQLError.createSQLException(SQLError.java:963)\n"
                    "	at com.mysql.jdbc.MysqlIO.checkErrorPacket(MysqlIO.java:3966)\n"
                    "	at com.mysql.jdbc.MysqlIO.checkErrorPacket(MysqlIO.java:3902)\n"
                    "	at com.mysql.jdbc.MysqlIO.sendCommand(MysqlIO.java:2526)\n"
                    "	at com.mysql.jdbc.MysqlIO.sqlQueryDirect(MysqlIO.java:2673)\n"
                    "	at com.mysql.jdbc.ConnectionImpl.execSQL(ConnectionImpl.java:2549)\n"
                    "	at com.mysql.jdbc.PreparedStatement.executeInternal(PreparedStatement.java:1861)\n"
                    "	at com.mysql.jdbc.PreparedStatement.executeUpdateInternal(PreparedStatement.java:2073)\n"
                    "	at com.mysql.jdbc.PreparedStatement.executeUpdateInternal(PreparedStatement.java:2009)\n"
                    "	at com.mysql.jdbc.PreparedStatement.executeLargeUpdate(PreparedStatement.java:5098)\n"
                    "	at com.mysql.jdbc.PreparedStatement.executeUpdate(PreparedStatement.java:1994)\n"
                    "	at com.zaxxer.hikari.pool.ProxyPreparedStatement.executeUpdate(ProxyPreparedStatement.java:61)\n"
                    "	at com.zaxxer.hikari.pool.HikariProxyPreparedStatement.executeUpdate(HikariProxyPreparedStatement.java)\n"
                    "	at com.clover.serverkit.persistence.db.sharding.TenancyCheckedPreparedStatement$$Lambda$322/1658573398.execute(Unknown Source)\n"
                    "	at com.clover.serverkit.persistence.db.sharding.TenancyCheckedConnection.execute(TenancyCheckedConnection.java:130)\n"
                    "	at com.clover.serverkit.persistence.db.sharding.TenancyCheckedConnection.executeWriter(TenancyCheckedConnection.java:110)\n"
                    "	at com.clover.serverkit.persistence.db.sharding.TenancyCheckedPreparedStatement.executeUpdate(TenancyCheckedPreparedStatement.java:54)\n"
                    "	at com.clover.serverkit.persistence.db.ExecuteUpdate.execute(ExecuteUpdate.java:20)\n"
                    "	at com.clover.serverkit.persistence.db.DatabaseExecute.run(DatabaseExecute.java:37)\n"
                    "	... 16 more\n")
        save_setup_files(log_data)

        log_entries_as_strings = _get_log_entries_as_strings(test_log_path)
        self.assertEqual(log_data, next(log_entries_as_strings))


class TestParseLogEntriesIntoKeyValuePairs(unittest.TestCase):

    def setUp(self):
        self.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        for file_path in [test_log_path, test_log_offset_file_path]:
            if os.path.isfile(file_path):
                remove_file(file_path)

    def test_datetime_parsing(self):
        true_datetime = datetime(2018, 1, 30, 0, 0, 0, 3000)
        datetime_string = "2018-01-30 00:00:00.003"
        log_data = "[%s] [INFO] u= p= r= d= m= v= i= hm= hs= da= am= t= RolloutJob started (RolloutJob)" % datetime_string
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(true_datetime, log_entry_as_a_dict['datetime'])

    def test_empty_log_entry(self):
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm= hs= da= am= t= RolloutJob started (RolloutJob)\n"
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(None, log_entry_as_a_dict['uri'])

    def test_log_levels(self):
        for log_level in possible_log_levels:
            log_data = "[2018-01-30 00:00:00.003] [%s] u= p= r= d= m= v= i= hm= hs= da= am= t= RolloutJob started (RolloutJob)\n" % (log_level)
            save_setup_files(log_data)
            log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

            self.assertEqual(log_level, log_entry_as_a_dict['log_level'])

            self.setUp()  # Need to do this to have the pygtail cursor reset.

    def test_uri(self):
        uri = "/v3/merchants/DPA9VR0WM805Y/employees"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u=%s p= r= d= m= v= i= hm= hs= da= am= t= RolloutJob started (RolloutJob)\n" % uri
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(uri, log_entry_as_a_dict['uri'])

    def test_uri_pattern(self):
        uri_pattern = "/v3/merchants/{mId}/employees"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p=%s r= d= m= v= i= hm= hs= da= am= t= RolloutJob started (RolloutJob)\n" % uri_pattern
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(uri_pattern, log_entry_as_a_dict['uri_pattern'])

    def test_request_uuid(self):
        request_uuid = "84098095-7420-18a5-3e16-7c392ba98c64"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r=%s d= m= v= i= hm= hs= da= am= t= RolloutJob started (RolloutJob)\n" % request_uuid
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(request_uuid, log_entry_as_a_dict['request_uuid'])

    def test_device_uuid(self):
        device_uuid = "7412A5DAD2C24AB1B006B98DA6F6DD2C"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d=%s m= v= i= hm= hs= da= am= t= RolloutJob started (RolloutJob)\n" % device_uuid
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(device_uuid, log_entry_as_a_dict['device_uuid'])

    def test_merchant_id(self):
        merchant_id = "2278"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m=%s v= i= hm= hs= da= am= t= RolloutJob started (RolloutJob)\n" % merchant_id
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(merchant_id, log_entry_as_a_dict['merchant_id'])

    def test_version_id(self):
        version_id = "1914"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v=%s i= hm= hs= da= am= t= RolloutJob started (RolloutJob)\n" % version_id
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(version_id, log_entry_as_a_dict['version_id'])

    def test_request_ip(self):
        request_ip = "50.249.120.58"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i=%s hm= hs= da= am= t= RolloutJob started (RolloutJob)\n" % request_ip
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(request_ip, log_entry_as_a_dict['request_ip'])

    def test_http_method(self):
        for http_method in possible_http_methods:
            log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm=%s hs= da= am= t= RolloutJob started (RolloutJob)\n" % http_method
            save_setup_files(log_data)
            log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

            self.assertEqual(http_method, log_entry_as_a_dict['http_method'])

            self.setUp()  # Need to do this to have the pygtail cursor reset.

    def test_http_status(self):
        http_status = "200"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm= hs=%s da= am= t= RolloutJob started (RolloutJob)\n" % http_status
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(http_status, log_entry_as_a_dict['http_status'])

    def test_developer_app_id(self):
        developer_app_id = "123"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm= hs= da=%s am= t= RolloutJob started (RolloutJob)\n" % developer_app_id
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(developer_app_id, log_entry_as_a_dict['developer_app_id'])

    def test_auth_mechanism(self):
        for auth_mechanism in possible_auth_mechanisms:
            log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm= hs= da= am=%s t= RolloutJob started (RolloutJob)\n" % auth_mechanism
            save_setup_files(log_data)
            log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

            self.assertEqual(auth_mechanism, log_entry_as_a_dict['auth_mechanism'])

            self.setUp()  # Need to do this to have the pygtail cursor reset.

    def test_request_time(self):
        request_time = "3"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm= hs= da= am= t=%s RolloutJob started (RolloutJob)\n" % request_time
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(request_time, log_entry_as_a_dict['request_time'])

    def test_log_statement(self):
        log_statement = "RolloutJob started"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm= hs= da= am= t= %s (RolloutJob)\n" % log_statement
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(log_statement, log_entry_as_a_dict['log_statement'])

    def test_logging_class(self):
        logging_class = "FileRequestObjectLogger"
        log_data = "[2018-01-30 00:00:00.003] [INFO] u= p= r= d= m= v= i= hm= hs= da= am= t= RolloutJob started (%s)\n" % logging_class
        save_setup_files(log_data)
        log_entry_as_a_dict = self.get_next_log_entry_as_a_dict()

        self.assertEqual(logging_class, log_entry_as_a_dict['logging_class'])

    def get_next_log_entry_as_a_dict(self):
        log_entries_as_strings = _get_log_entries_as_strings(test_log_path)
        log_entry_as_a_string = next(log_entries_as_strings)
        log_entry_as_a_dict = get_dict_from_log_entry_as_a_string(log_entry_as_a_string)
        return log_entry_as_a_dict


if __name__ == '__main__':
    unittest.main()
