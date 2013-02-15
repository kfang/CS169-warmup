import unittest
import os
import testLib

class TestUnit(testLib.RestTestCase):
    """Issue a REST API request to run the unit tests, and analyze the result"""
    def testUnit(self):
        respData = self.makeRequest("/TESTAPI/unitTests", method="POST")
        self.assertTrue('output' in respData)
        print ("Unit tests output:\n"+
               "\n***** ".join(respData['output'].split("\n")))
        self.assertTrue('totalTests' in respData)
        print "***** Reported "+str(respData['totalTests'])+" unit tests"
        # When we test the actual project, we require at least 10 unit tests
        minimumTests = 10
        if "SAMPLE_APP" in os.environ:
            minimumTests = 4
        self.assertTrue(respData['totalTests'] >= minimumTests,
                        "at least "+str(minimumTests)+" unit tests. Found only "+str(respData['totalTests'])+". use SAMPLE_APP=1 if this is the sample app")
        self.assertEquals(0, respData['nrFailed'])

        
class TestAddUser(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testAdd1(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)

    
class TestLoginUser(testLib.RestTestCase):
    def testlogin(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'admin', 'password' : 'admin'})
        expected = {}
        expected['errCode'] = 1
        expected['count'] = 1
        self.assertDictEqual(expected, respData)

        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'admin', 'password' : 'admin'})
        expected['count'] = 2
        self.assertDictEqual(expected, respData)

class TestLoginCount(testLib.RestTestCase):
    def testLoginCount(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'admin', 'password' : 'admin'})
        expected = {}
        expected['errCode'] = 1
        expected['count'] = 1
        self.assertDictEqual(expected, respData)

        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'foo', 'password' : 'bar'})
        expected = {}
        expected['errCode'] = 1
        expected['count'] = 1
        self.assertDictEqual(expected, respData)

        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'admin', 'password' : 'admin'})
        expected['count'] = 2
        self.assertDictEqual(expected, respData)
        respData = self.makeRequest("/users/login", method="POST", data={'user':'admin', 'password':'admin'})
        expected['count'] = 3
        self.assertDictEqual(expected, respData)
        respData = self.makeRequest("/users/login", method="POST", data={'user':'admin', 'password':'admin'})
        expected['count'] = 4
        self.assertDictEqual(expected, respData)

        respData = self.makeRequest("/users/login", method="POST", data={'user':'foo', 'password':'bar'})
        expected['count'] = 2
        self.assertDictEqual(expected, respData)
        respData = self.makeRequest("/users/login", method="POST", data={'user':'foo', 'password':'bar'})
        expected['count'] = 3
        self.assertDictEqual(expected, respData)
        respData = self.makeRequest("/users/login", method="POST", data={'user':'foo', 'password':'bar'})
        expected['count'] = 4
        self.assertDictEqual(expected, respData)

class TestBadPassLogin(testLib.RestTestCase):
    def testBadPass(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'admin', 'password' : 'admin'})
        expected = {}
        expected['errCode'] = 1
        expected['count'] = 1
        self.assertDictEqual(expected, respData)

        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'admin', 'password' : 'foo'})
        expected = {}
        expected['errCode'] = -1
        self.assertDictEqual(expected, respData)

class TestBadUserLogin(testLib.RestTestCase):
    def testBadUser(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'admin', 'password' : 'admin'})
        expected = {}
        expected['errCode'] = 1
        expected['count'] = 1
        self.assertDictEqual(expected, respData)

        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'foo', 'password' : 'admin'})
        expected = {}
        expected['errCode'] = -1
        self.assertDictEqual(expected, respData)

class TestBadUserAdd(testLib.RestTestCase):
    def testBadUser(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : '', 'password' : 'admin'})
        expected = {}
        expected['errCode'] = -3
        self.assertDictEqual(expected, respData)

class TestBadPassAdd(testLib.RestTestCase):
    def testBadPass(self):
        password = ''
        for n in range(200):
            password += 'a'

        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'admin', 'password' : password})
        expected = {}
        expected['errCode'] = -4
        self.assertDictEqual(expected, respData)

class TestExistUserAdd(testLib.RestTestCase):
    def testExistUser(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'admin', 'password' : 'admin'})
        expected = {}
        expected['errCode'] = 1
        expected['count'] = 1
        self.assertDictEqual(expected, respData)

        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'admin', 'password' : 'admin'})
        expected = {}
        expected['errCode'] = -2
        self.assertDictEqual(expected, respData)