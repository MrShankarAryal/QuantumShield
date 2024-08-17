import unittest
from core.behavior_analysis import BehaviorAnalysis

class TestBehaviorAnalysis(unittest.TestCase):
    def test_prediction(self):
        analysis = BehaviorAnalysis()
        features = [1, 0, 0, 1, 1, 0]  # Example features
        prediction = analysis.predict(features)
        self.assertIn(prediction, [0, 1])  # 0 = Normal, 1 = Anomaly

if __name__ == "__main__":
    unittest.main()
