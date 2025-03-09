import exploit
from lxml import etree
from lxml import html
import consumer
import producer
import json
import unittest

evil = html.parse('../materials/evilcorp.html')


class TestMrRobot(unittest.TestCase):

    def test_exploit_title_change(self):
        exploit.title_change(evil)
        self.assertEqual(next(evil.iter('title')).text, 'Evil Corp - Stealing your money every day')

    def test_hacked_announcement(self):
        name: str = ''
        pronoun: str = ''
        person = evil.findall('.//span[@class]')
        for atr in person:
            if atr.get('class') == 'pronoun':
                name = atr.tail
                pronoun = atr.text
        exploit.hacked_announcement(evil)
        self.assertEqual(next(evil.iter('h1')).text, pronoun + name + ', you are hacked!')

    def test_replace_link(self):
        exploit.replace_link(evil)
        link = next(evil.iter('a'))
        self.assertEqual(link.get('href'), 'https://mrrobot.fandom.com/wiki/Fsociety')
        self.assertEqual(link.text, 'Fsociety')

    def test_insert_element(self):
        script = etree.fromstring('''
        <script>
        hacked = function() {
            alert('hacked');
        }
        window.addEventListener('load', 
            function() { 
                var f = document.querySelector("form");
                f.setAttribute("onsubmit", "hacked()");
            },
            false
        );
        </script>
    ''')
        exploit.insert_element(evil, script)
        link = next(evil.iter('script'))
        self.assertEqual(link, script)

    def test_producer_create_account_number(self):
        number = producer.create_account_number()
        self.assertIsInstance(number, int)
        self.assertEqual(len(str(number)), 10)

    def test_producer_create_amount(self):
        number = producer.create_amount()
        self.assertGreaterEqual(number, -10000)
        self.assertLessEqual(number, 10000)

    def test_producer_create_message(self):
        msg = producer.create_message(5, 5, 10)
        data = json.loads(msg)
        self.assertEqual(data['metadata']['from'], 5)
        self.assertEqual(data['metadata']['to'], 5)
        self.assertEqual(data['amount'], 10)


if __name__ == '__main__':
    unittest.main()
