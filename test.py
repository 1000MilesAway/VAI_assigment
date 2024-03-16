import requests
import json
import unittest

headers = {'Content-Type': 'application/json'}
url = "http://localhost:5000/product"



class Testing(unittest.TestCase):  
    def test_1_add(self): 
        data = {"name":"Product", "description":"This is an product", "price": 17.50, "category": "Product"}
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        assert resp.status_code == 201  
        
    def test_2_get(self): 
        resp = requests.get("http://localhost:5000/product/1", headers=headers)
        assert resp.status_code == 200
        
    def test_3_put(self): 
        data = {"name":"Updated Product", "description":"This is an updated product", "price": 24.50, "category": "Updated"}
        resp = requests.put("http://localhost:5000/product/1", headers=headers, data=json.dumps(data))
        assert resp.status_code == 200
        
    def test_4_search(self): 
        resp = requests.get(f"{url}/search?name=Product&description=product'", headers=headers)
        assert resp.status_code == 200

    def test_5_delete(self): 
        resp = requests.delete(f"{url}/1", headers=headers)
        assert resp.status_code == 200
    

if __name__ == '__main__':
    unittest.main()
