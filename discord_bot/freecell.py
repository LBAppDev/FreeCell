import random

class Card:
    rank_map = { 'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13 }
    suit_map = {'H': '♥', 'D': '♦', 'C': '♣', 'S': '♠'}

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit_map[self.suit]}"

    def is_red(self):
        return self.suit in ['H', 'D']

    def is_black(self):
        return self.suit in ['C', 'S']

class FreeCell:
    def __init__(self):
        self.foundations = [[] for _ in range(4)]
        self.free_cells = [None] * 4
        self.cascades = [[] for _ in range(8)]
        self.deck = self._create_deck()
        self._deal_cards()

    def _create_deck(self):
        suits = ['H', 'D', 'C', 'S']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        return [Card(suit, rank) for suit in suits for rank in ranks]

    def _deal_cards(self):
        random.shuffle(self.deck)
        for i, card in enumerate(self.deck):
            self.cascades[i % 8].append(card)

    def get_game_state(self):
        RED = '\u001b[31m'
        WHITE = '\u001b[37m'
        RESET = '\u001b[0m'

        def card_str_boxed(card):
            if not card:
                return '[   ]'
            color = RED if card.is_red() else WHITE
            suit = Card.suit_map[card.suit]
            rank = card.rank.rjust(2)
            return f'{color}[{rank}{suit}]{RESET}'

        lines = []

        f_str = ' '.join(card_str_boxed(f[-1]) if f else '[   ]' for f in self.foundations)
        c_str = ' '.join(card_str_boxed(c) for c in self.free_cells)
        lines.append(f'Foundations: {f_str}')
        lines.append(f'Free Cells:  {c_str}')
        lines.append('')

        lines.append('   c1    c2    c3    c4    c5    c6    c7    c8')
        lines.append('  ' + '----  ' * 8)

        max_len = max(len(c) for c in self.cascades) if self.cascades else 0
        for i in range(max_len):
            row_list = []
            for cascade in self.cascades:
                if i < len(cascade):
                    card = cascade[i]
                    color = RED if card.is_red() else WHITE
                    suit = Card.suit_map[card.suit]
                    rank = card.rank.rjust(2)
                    row_list.append(f' {color}{rank}{suit}{RESET}  ')
                else:
                    row_list.append('      ') # 6 spaces
            lines.append(''.join(row_list))

        return '```ansi\n' + '\n'.join(lines) + '\n```'

    def get_card(self, col, card_index=None):
        if col.startswith('c'):
            cascade_index = int(col[1:]) - 1
            if not self.cascades[cascade_index]:
                return None, None
            if card_index is None:
                return self.cascades[cascade_index][-1], len(self.cascades[cascade_index]) -1
            else:
                return self.cascades[cascade_index][card_index], card_index
        elif col.startswith('f'):
            free_cell_index = int(col[1:]) - 1
            return self.free_cells[free_cell_index], free_cell_index
        return None, None
        
    def _validate_move(self, card, to_col):
        if to_col.startswith('f'):
            to_free_cell_index = int(to_col[1:]) - 1
            if self.free_cells[to_free_cell_index] is not None:
                raise ValueError("Target free cell is not empty.")
            return

        if to_col.startswith('o'):
            to_foundation_index = int(to_col[1:]) - 1
            foundation = self.foundations[to_foundation_index]
            if not foundation:
                if card.rank != 'A':
                    raise ValueError("Only an Ace can start a foundation.")
            else:
                top_card = foundation[-1]
                if top_card.suit != card.suit or Card.rank_map[top_card.rank] != Card.rank_map[card.rank] - 1:
                    raise ValueError("Card cannot be placed on foundation.")
            return

        if to_col.startswith('c'):
            to_cascade_index = int(to_col[1:]) - 1
            cascade = self.cascades[to_cascade_index]
            if not cascade:
                return
            
            top_card = cascade[-1]
            if top_card.is_red() == card.is_red():
                raise ValueError("Cards in a cascade must have alternating colors.")
            
            if Card.rank_map[top_card.rank] != Card.rank_map[card.rank] + 1:
                raise ValueError("Card ranks must be in descending order.")
            return

    def move(self, from_col, to_col, card_index=None):
        card, actual_card_index = self.get_card(from_col, card_index)

        if card is None:
            raise ValueError("Invalid source.")

        if from_col.startswith('c') and actual_card_index is not None and actual_card_index != len(self.cascades[int(from_col[1:])-1]) -1:
             raise ValueError("Only the top card of a cascade can be moved.")


        self._validate_move(card, to_col)

        # Remove card from source
        if from_col.startswith('c'):
            self.cascades[int(from_col[1:])-1].pop()
        elif from_col.startswith('f'):
            self.free_cells[int(from_col[1:])-1] = None

        # Add card to destination
        if to_col.startswith('c'):
            self.cascades[int(to_col[1:])-1].append(card)
        elif to_col.startswith('f'):
            self.free_cells[int(to_col[1:])-1] = card
        elif to_col.startswith('o'):
            self.foundations[int(to_col[1:])-1].append(card)


    def check_win(self):
        return all(len(f) == 13 for f in self.foundations)
