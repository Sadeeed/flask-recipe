from unittest import TestCase
from app import create_app


class BaseTest(TestCase):
    def setUp(self) -> None:
        app = create_app()
        app.testing = True
        self.app = app.test_client
        
    # def test_something(self):
    #     self.assertEqual(True, False)  # add assertion here

# if __name__ == '__main__':
#     unittest.main()
