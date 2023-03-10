import random


class Pokemon:
    # existing code omitted for brevity

    def choose_move(self, opponent):
        best_move = None
        best_move_score = -1

        # Iterate over all available moves
        for move_name in self.get_info()['moves']:
            move = Move(move_name)

            # Calculate the score for this move
            score = 0

            # Type advantage
            type_score = move.get_type_score(opponent)
            score += type_score

            # Move power
            score += move.power

            # Accuracy
            score += move.accuracy

            # Status effect
            if move.status_effect is not None:
                score += move.status_effect.get_effect_score(self, opponent)

            # Update the best move if this move has a higher score
            if score > best_move_score:
                best_move = move
                best_move_score = score

        # Return the best move or a random move if no moves available
        if best_move is None:
            return random.choice(self.get_info()['moves'])
        else:
            return best_move.name