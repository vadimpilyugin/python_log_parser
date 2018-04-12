import unittest
import log_formats as fmt
import fields
import re
import excp
import service as srv
import loader as ld
import parser as p
import aggregation as agg

class TestLogFormat(unittest.TestCase):
  def setUp(self):
    self.re_str1 = r'(?P<foo>\S+) (?P<bar>\S+)'
    self.re_str2 = r'foo\d+'
    self.str1 = 'foobar foobaz'
    self.str2 = 'foo123'
    self.str3 = 'foobar   '
    self.service1 = 'foo'
    self.hsh1 = {
      'foo':'foobar', 
      'bar':'foobaz', 
      fields.SERVICE:self.service1
    }
    self.format_name1 = 'FooFormat'
    self.regex1 = re.compile(self.re_str1)
    self.regex2 = re.compile(self.re_str2)
    self.log_format1 = fmt.LogFormat(
      name=self.format_name1, 
      regex=self.regex1, 
      service=self.service1
    )
    log_formats = ld.load_log_formats(ld.content('test_log_formats.yml'))
    self.apache_format = log_formats.log_formats[0]
    self.apache_s = '141.8.142.23 - - [09/Oct/2016:06:35:46 +0300] "GET /robots.txt HTTP/1.0" 404 289 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)" - - old.parallel.ru'

  def test_create_log_format(self):
    fmt.LogFormat(
      name=self.format_name1, 
      regex=self.regex1, 
      service=self.service1
    )

  def test_parse_log_format(self):
    hsh = self.log_format1.parse(self.str1)
    self.assertEqual(hsh,self.hsh1)

  def test_raise_on_service_missing(self):
    with self.assertRaises(excp.LogFormatException, msg=fmt.NO_SERVICE):
      f = fmt.LogFormat(
        name=self.format_name1, 
        regex=self.regex1, 
      )

  def test_regex_with_service(self):
    f = fmt.LogFormat(name='foo',regex=re.compile(r'(?P<__SERVICE__>\S+) (?P<digits>\d\d)'))
    self.assertEqual(f.parse('foobar 12'), {fields.SERVICE:'foobar', 'digits':'12'})

  def test_wrong_parse(self):
    self.assertIsNone(self.log_format1.parse(self.str3))

  def test_apache_format(self):
    match_data = self.apache_format.parse(self.apache_s)
    self.assertIsNotNone(match_data)
    self.assertEqual(match_data['user_ip'], '141.8.142.23')
    self.assertEqual(match_data['path'], '/robots.txt')
    self.assertEqual(match_data['method'], 'GET')
    self.assertEqual(match_data['code'], '404')


class TestLogFormatSet(unittest.TestCase):
  def setUp(self):
    self.f1 = fmt.LogFormat(
      name='FooFormat1',
      regex=re.compile(r'\d\d\d\d (?P<__SERVICE__>\w+) \d\d\.\d\d\d\d'),
    )
    self.f2 = fmt.LogFormat(
      name='FooFormat2',
      regex=re.compile(r'\d\d--\d\d (?P<__SERVICE__>\w+) \d\d-\d\d-\d\d\d\d'),
    )
    self.f3 = fmt.LogFormat(
      name='FooFormat3',
      regex=re.compile(r'\d\d\s\d\d (?P<__SERVICE__>\w+) \d\d\s\d\d\s\d\d\d\d'),
    )
    self.p = fmt.LogFormatSet([self.f1,self.f2,self.f3])
    self.lines1 = [
      '1359 sshd 12.2014',
      '4241 sshd 13.2014',
      '5752 sshd 14.2014',
      '9658 sshd 15.2014',
    ]
    self.lines2 = [
      '13--59 sshd 12-01-2014',
      '42--41 sshd 13-01-2014',
      '57--52 sshd 14-01-2014',
      '96--58 sshd 15-01-2014',
    ]

  def test_parsing(self):
    self.assertEqual(self.p.parse(self.lines1[0]), self.f1.parse(self.lines1[0]))

  def test_lines(self):
    for line in self.lines1:
      self.assertEqual(self.f1.parse(line), {fields.SERVICE:'sshd'})
    for line in self.lines2:
      self.assertEqual(self.f2.parse(line), {fields.SERVICE:'sshd'})

  def test_caching(self):
    self.p.parse(self.lines1[0])
    self.assertEqual(self.p.cached_format, self.f1)
    self.p.parse(self.lines1[1])
    self.assertEqual(self.p.cached_format, self.f1)
    self.p.parse(self.lines2[0])
    self.assertEqual(self.p.cached_format, self.f2)

class TestTemplate(unittest.TestCase):
  def setUp(self):
    self.regex_s = r'Connection from (?P<user_ip>\d+\.\d+\.\d+\.\d+) port (?P<user_port>\d+)'
    self.regex = re.compile(
      self.regex_s
    )
    self.category = 'New connection'
    self.level = 'Info'
    self.template_id = 1
    self.template = srv.Template(
      regex_s=self.regex_s,
      category=self.category,
      level=self.level,
      template_id=self.template_id
    )
    self.s = 'Connection from 1.1.1.1 port 1234'

  def test_parse(self):
    self.assertEqual(self.template.parse(self.s), {
      fields.TEMPLATE_REGEX : self.regex_s,
      fields.LEVEL : self.level,
      fields.TEMPLATE_CATEGORY : self.category,
      fields.TEMPLATE_ID : self.template_id,
      'user_ip' : '1.1.1.1',
      'user_port' : '1234'
    })

class ServiceTemplates(unittest.TestCase):
  def setUp(self):
    self.t1 = srv.Template(
      regex_s=r'Connection from (?P<user_ip>\d+\.\d+\.\d+\.\d+) port (?P<user_port>\d+)',
      category='New connection',
      level='Info',
      template_id=1
    )
    self.t2 = srv.Template(
      regex_s=r'Disconnected from (?P<user_ip>\d+\.\d+\.\d+\.\d+) port (?P<user_port>\d+)',
      category='Disconnect',
      level='Info',
      template_id=2
    )
    self.t3 = srv.Template(
      regex_s=r'fatal: Read from socket failed: Connection reset by peer',
      category='Connection reset',
      level='Error',
      template_id=3
    )
    self.templates = srv.ServiceTemplates([self.t1, self.t2, self.t3])
    self.line1 = 'Connection from 1.1.1.1 port 1234'
    self.line2 = 'Disconnected from 1.1.1.1 port 1234'
    self.line3 = 'fatal: Read from socket failed: Connection reset by peer [preauth]'

  def test_parse(self):
    self.assertEqual(self.templates.parse(self.line1),self.t1.parse(self.line1))
    self.assertEqual(self.templates.parse(self.line2),self.t2.parse(self.line2))
    self.assertEqual(self.templates.parse(self.line3),self.t3.parse(self.line3))

  def test_sort(self):
    for i in range(0,srv.SORT_INTERVAL):
      self.templates.parse(self.line3)
      self.templates.parse(self.line3)
      self.templates.parse(self.line2)
    self.assertEqual(self.templates.templates, [self.t3, self.t2, self.t1])

class TestService(unittest.TestCase):
  def setUp(self):
    self.service1 = srv.Service(
      regex=re.compile(r'foo\d+'), 
      name='foo', 
    )

  def test_is_service(self):
    self.assertTrue(self.service1.is_service('foo123'))
    self.assertFalse(self.service1.is_service('bar123'))

class TestServiceSet(unittest.TestCase):
  def setUp(self):
    self.s1 = srv.Service(
      regex=re.compile(r'foo\d+'),
      name='foo'
    )
    self.s2 = srv.Service(
      regex=re.compile(r'bar\d+'),
      name='bar'
    )
    self.s3 = srv.Service(
      regex=re.compile(r'baz\d+'),
      name='baz'
    )
    self.ss = srv.ServiceSet(
      services=[self.s1,self.s2,self.s3]
    )

  def test_find_service(self):
    self.assertEqual(self.ss.find_service('foo123'), self.s1)
    self.assertEqual(self.ss.find_service('bar123'), self.s2)
    self.assertEqual(self.ss.find_service('baz123'), self.s3)
    self.assertIsNone(self.ss.find_service('foobar123'))

  def test_caching(self):
    self.assertFalse('foo1234' in self.ss.cached_services)
    self.ss.find_service('foo1234')
    self.assertTrue('foo1234' in self.ss.cached_services)

  def test_service_not_found(self):
    self.assertIsNone(self.ss.find_service('apache'))

class TestParser(unittest.TestCase):
  def setUp(self):
    self.log_format_set = ld.load_log_formats(ld.content('test_log_formats.yml'))
    self.service_set = ld.load_all_services('test_templates')
    self.p = p.Parser(self.log_format_set, self.service_set)
    self.loglines = [
      'May 18 11:16:29 93.180.9.161 motion: [1] [NTC] [EVT] event_new_video FPS 2',
      'May 18 11:16:31 93.180.9.161 motion: [1] [NTC] [EVT] Camera 2 started: motion detection',
      '141.8.142.23 - - [09/Oct/2016:06:35:46 +0300] "GET /robots.txt HTTP/1.0" 404 289 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)" - - old.parallel.ru',
      '217.69.133.28 - - [09/Oct/2016:06:53:14 +0300] "GET /tech/tech_dev/MPIcourse/tasks5.html HTTP/1.0" 200 794 "-" "Mozilla/5.0 (compatible; Linux x86_64; Mail.RU_Bot/2.0; +http://go.mail.ru/help/robots)" - - old.parallel.ru',
      'Dec 11 07:37:56 newserv sshd[14495]: Connection from 42.7.26.60 port 2838 on 93.180.9.8 port 22',
      'Dec 11 07:38:16 newserv sshd[14495]: Disconnected from user root 42.7.26.60',
    ]
    self.bad_loglines = [
      'Motion detected: [1] [NTC] [EVT] event_new_video FPS 2',
      'Dec 11 07:37:56 newserv kernel[14495]: Connection from 42.7.26.60 port 2838 on 93.180.9.8 port 22',
      'Dec 11 07:38:16 newserv sshd[14495]: Disconnecting from user root 42.7.26.60',
    ]
    self.errnos = [
      p.NO_FORMAT,
      p.NO_SERVICE,
      p.NO_TEMPLATE
    ]

  def test_parse(self):
    for logline in self.loglines:
      errno, reason, match_data = self.p.parse(logline)
      self.assertIsNone(reason)
      self.assertIsNotNone(match_data)
      self.assertEqual(errno, p.OK)

  def test_bad_parse(self):
    for i in range(0,len(self.errnos)):
      logline = self.bad_loglines[i]
      errno, reason, match_data = self.p.parse(logline)
      self.assertEqual(errno, self.errnos[i])

class TestAggregation(unittest.TestCase):
  def setUp(self):
    self.agg = agg.Aggregation(
      name="Aggregation 1",
      keys=["key1", "key2"]
    )
    self.items = [
      {"key1":"2", "key2":"foo"},
      {"key1":"2", "key2":"foo", "key3":'baz'},
      {"key1":"3", "key2":"bar"},
      {"key1":"3", "key2":"bar"},
      {"key1":"3", "key2":"baz"},
      {"key1":"3", "key3":"baz"},
      {"key4":"3", "key2":"baz"},
    ]

  def test_aggregation(self):
    for i in self.items:
      self.agg.insert(i)
    self.assertEqual(
      self.agg.get_distrib()[fields.ARRAY],
      [
        ['3', 
          [
            ['bar', 2], 
            ['baz', 1]
          ]
        ], 
        ['2', 
          [
            ['foo', 2]
          ]
        ]
      ]
    )
    self.assertEqual(self.agg.get_distrib()[fields.WEIGHT], 5)


if __name__ == '__main__':
  unittest.main()