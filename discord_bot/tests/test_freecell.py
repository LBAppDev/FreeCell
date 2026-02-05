import unittest
import sys
import os

# Add the parent directory to the path to allow imports from the discord_bot directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from freecell import FreeCell, Card

class TestFreeCell(unittest.TestCase):

    def setUp(self):
        self.game = FreeCell()

    def test_move_to_empty_free_cell(self):
        top_card_c1 = self.game.cascades[0][-1]
        self.game.move('c1', 'f1')
        self.assertEqual(self.game.free_cells[0], top_card_c1)

    def test_move_to_occupied_free_cell(self):
        self.game.move('c1', 'f1')
        with self.assertRaisesRegex(ValueError, "Target free cell is not empty."):
            self.game.move('c2', 'f1')

    def test_move_ace_to_foundation(self):
        # Manually place an Ace at the top of a cascade
        self.game.cascades[0].append(Card('S', 'A'))
        self.game.move('c1', 'o1')
        self.assertEqual(len(self.game.foundations[0]), 1)
        self.assertEqual(self.game.foundations[0][0].rank, 'A')

    def test_move_invalid_to_foundation(self):
        # Manually place a non-Ace at the top of a cascade
        self.game.cascades[0].append(Card('S', 'K'))
        with self.assertRaisesRegex(ValueError, "Only an Ace can start a foundation."):
            self.game.move('c1', 'o1')
    
    def test_cascade_to_cascade_valid(self):
        # Manually set up a valid move scenario
        self.game.cascades[0] = [Card('S', 'K')]
        self.game.cascades[1] = [Card('H', 'Q')]
        self.game.move('c2', 'c1')
        self.assertEqual(len(self.game.cascades[0]), 2)
        self.assertEqual(str(self.game.cascades[0][-1]), 'Q♥')

    def test_cascade_to_cascade_invalid_color(self):
        self.game.cascades[0] = [Card('S', 'K')]
        self.game.cascades[1] = [Card('C', 'Q')] # Same color
        with self.assertRaisesRegex(ValueError, "Cards in a cascade must have alternating colors."):
            self.game.move('c2', 'c1')

    def test_cascade_to_cascade_invalid_rank(self):
        self.game.cascades[0] = [Card('S', 'K')]
        self.game.cascades[1] = [Card('H', 'J')] # Invalid rank
        with self.assertRaisesRegex(ValueError, "Card ranks must be in descending order."):
            self.game.move('c2', 'c1')

    def test_win_condition(self):
        self.assertFalse(self.game.check_win())
        
        # Manually create a winning state
        suits = ['H', 'D', 'C', 'S']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        for i in range(4):
            for rank in ranks:
                self.game.foundations[i].append(Card(suits[i], rank))
        
        self.assertTrue(self.game.check_win())

if __name__ == '__main__':
    unittest.main()
