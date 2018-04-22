class ApiTestsMixin(object):
    def assertApiResultsAreEmpty(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'], [])

    def assertApiResultsEqual(self, response, items):
        self.assertEqual(response.status_code, 200)
        results_ids = [r['id'] for r in response.json()['results']]
        items_ids = [i.id for i in items]
        self.assertEqual(results_ids, items_ids)

    def assertInApiResults(self, response, item):
        self.assertEqual(response.status_code, 200)
        results_ids = [r['id'] for r in response.json()['results']]
        self.assertIn(item.id, results_ids)

    def assertNotInApiResults(self, response, item):
        self.assertEqual(response.status_code, 200)
        results_ids = [r['id'] for r in response.json()['results']]
        self.assertNotIn(item.id, results_ids)
