import copy,json,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from build import build
from validate import validate,inspect
from package import package
from svg_core import SVG,wrap,width
class PipelineTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.out=self.root/'out';self.d=json.loads((ROOT/'examples/deck.json').read_text(encoding='utf-8'))
 def tearDown(self):self.tmp.cleanup()
 def test_all_layouts_and_archive(self):
  self.assertEqual(build(self.d,self.out),5);self.assertTrue(validate(self.out)['passed']);archive=self.root/'slides.zip';self.assertEqual(package(self.out,archive),5)
  with zipfile.ZipFile(archive) as z:self.assertEqual(len(z.namelist()),8);self.assertIsNone(z.testzip())
 def test_no_overwrite(self):
  build(self.d,self.out)
  with self.assertRaises(ValueError):build(self.d,self.out)
 def test_unknown_evidence(self):
  self.d['slides'][0]['evidence_ids']=['E999']
  with self.assertRaises(ValueError):build(self.d,self.out)
 def test_overflow_rejected(self):
  self.d['slides'][0]['notes'][0]['body']='过长文字'*1000
  with self.assertRaises(ValueError):build(self.d,self.out)
  self.assertFalse(self.out.exists())
 def test_xml_escape(self):
  s=SVG('A & B < C','',1,'测试');s.conclusion('A & B');p=self.root/'test.svg';s.write(p);self.assertIn('A &amp; B &lt; C',p.read_text());self.assertFalse(inspect(p)['errors'])
 def test_external_image_rejected(self):
  build(self.d,self.out);p=self.out/'01-architecture.svg';p.write_text(p.read_text().replace('</svg>','<image href="https://example.com/a.png"/></svg>'));self.assertFalse(validate(self.out)['passed'])
  with self.assertRaises(ValueError):package(self.out,self.root/'bad.zip')
 def test_invalid_color(self):
  build(self.d,self.out);p=self.out/'01-architecture.svg';p.write_text(p.read_text().replace('#0070c0','#123456'));self.assertFalse(validate(self.out)['passed'])
 def test_missing_file(self):
  build(self.d,self.out);(self.out/'01-architecture.svg').unlink();self.assertFalse(validate(self.out)['passed'])
 def test_wrap(self):
  self.assertTrue(all(width(x,12)<=100 for x in wrap('中文 long_identifier_with_very_long_word 测试',12,100)))
if __name__=='__main__':unittest.main()
