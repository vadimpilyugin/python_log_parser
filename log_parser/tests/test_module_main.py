# import unittest
# from log_parser import module_main as main

# class TestLogFormat(unittest.TestCase):
#   def test_search_repeated_subseq(self):
#     self.assertEqual(
#       main.search_repeated_subseq([498, 438, 450, 438, 491, 487, 446, 422]),
#       []
#     )
    
#   def test_repeat_filter(self):
#     self.assertEqual(
#       list(main.filter_for_repeats([(1,2,3,4,5,1,2,3,4)])),
#       [(1,2,3,4)]
#     )
#     self.assertEqual(
#       list(main.filter_for_repeats([(1,2,3,4,5,1,2,3,4,3,1,2,3,4)])),
#       [(1,2,3,4)]
#     )
#     self.assertEqual(
#       list(main.filter_for_repeats([
#         (498, 438, 450, 438, 491, 487, 446, 
#           422, 438, 498, 438, 450, 438, 491, 
#           487, 446, 422, 498, 438, 450, 438, 
#           491, 487, 446, 422)
#       ])),
#       [(498, 438, 450, 438, 491, 487, 446, 422)]
#     )
#     self.assertEqual(
#       list(main.filter_for_repeats([(498, 420, 433, 428, 424, 497, 495, 433)])),
#       [(498, 420, 433, 428, 424, 497, 495, 433)]
#     )

#   def test_rotate_filter(self):
#     self.assertEqual(
#       list(main.filter_for_rotations([(1,2,3,4),(2,3,4,1),(1,2,3,4,5),(4,3,1,2),(3,4,1,2)])),
#       [(1,2,3,4),(1,2,3,4,5),(4,3,1,2)]
#     )

#   def test_tandem_filter(self):
#     self.assertEqual(
#       list(main.filter_for_tandems([(1,1,2,1,3,2,1,2,3,4,1,2,3,4,1,2,3,4,5,3,1,2,3,4)])),
#       [(1,2,3,4)]
#     )
#     self.assertEqual(
#       list(main.filter_for_tandems([
#         (498, 438, 450, 438, 491, 487, 446, 
#           422, 438, 498, 438, 450, 438, 491, 
#           487, 446, 422, 498, 438, 450, 438, 
#           491, 487, 446, 422)])),
#       [(498, 438, 450, 438, 491, 487, 446, 422)]
#     )

#   def test_cyclic_levenstein(self):
#     k1 = (498, 438, 450, 438, 491, 487, 446, 422)
#     k2 = (491, 487, 446, 422, 498, 450, 438, 431)
#     self.assertTrue(
#       main.cyclic_levenstein_equiv(k1,k2,dist=2)
#     )

# if __name__ == '__main__':
#   unittest.main()
