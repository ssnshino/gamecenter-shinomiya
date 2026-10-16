import unittest,importlib.util,copy
from pathlib import Path
s=importlib.util.spec_from_file_location('review',Path(__file__).with_name('review-external-cleanup.py'));r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
class ReviewTests(unittest.TestCase):
 def setUp(self):
  self.a={'containers':[{'name':n,'id':i,'image':r.IMAGE,'running':False,'state':'exited','readonly':True,'labels':{'com.docker.compose.project':'queens-checker'},'mounts':[{'Type':'bind','Source':'/home/shino/source/labs/aladdin-master-restart-20261016/checker','Destination':'/proof','RW':False}]} for n,i in r.APPROVED.items()]+[{'name':'/protected','id':'unchanged'}],'runtime':[{'sha256':'original'}]};self.b=copy.deepcopy(self.a);self.b['containers']=self.b['containers'][-1:]
 def test_exact_review_and_no_original_mutation(self):
  orig=copy.deepcopy(self.a);v=r.reviewed(self.a,self.b);self.assertEqual(v['containers'],self.b['containers']);self.assertEqual(self.a,orig);self.assertEqual(v['runtime'],orig['runtime'])
 def test_running_rejected(self):
  self.a['containers'][0]['running']=True
  with self.assertRaises(ValueError):r.reviewed(self.a,self.b)
 def test_wrong_identity_rejected(self):
  self.a['containers'][0]['id']='other'
  with self.assertRaises(ValueError):r.reviewed(self.a,self.b)
 def test_writable_mount_rejected(self):
  self.a['containers'][0]['mounts'][0]['RW']=True
  with self.assertRaises(ValueError):r.reviewed(self.a,self.b)
 def test_other_service_change_rejected(self):
  self.b['containers'][0]['id']='changed'
  with self.assertRaises(ValueError):r.reviewed(self.a,self.b)
 def test_extra_container_rejected(self):
  self.b['containers'].append({'name':'/new'})
  with self.assertRaises(ValueError):r.reviewed(self.a,self.b)
 def test_not_removed_rejected(self):
  self.b['containers'].append(self.a['containers'][0])
  with self.assertRaises(ValueError):r.reviewed(self.a,self.b)
if __name__=='__main__':unittest.main()
