import otree
from . import *


class PlayerBot(Bot):

    def play_round(self):
        # If there is only one bot, it should send the message if at least 2 out of the three real players have also sent it

        # Majority of real players send the message -> expect bot to also send message
        # if self.player.id_in_group == 1:
        #     self.player.participant.is_dropout = True
        #     yield Submission(ChooseMessage, dict(message_chosen=2),timeout_happened=True)
        # else:
        #     yield ChooseMessage, dict(message_chosen=1)

        # Majority of real players don't send the message -> expect bot to also not send message
        # if self.player.id_in_group == 1:
        #     self.player.participant.is_dropout = True
        #     yield Submission(ChooseMessage, dict(message_chosen=1), timeout_happened=True)
        # elif self.player.id_in_group == 2:
        #     yield ChooseMessage, dict(message_chosen=1)
        # elif self.player.id_in_group == 3:
        #     yield ChooseMessage, dict(message_chosen=2)
        # elif self.player.id_in_group == 4:
        #     yield ChooseMessage, dict(message_chosen=2)

        # If there are 2 bots and 2 players and one real player has sent the message, one bot should also send the message and the other not

        # 1 or 2 real players send the message -> 1 bot sends the message and the other not
        # if self.player.id_in_group == 1 or self.player.id_in_group == 2:
        #     self.player.participant.is_dropout = True
        #     yield Submission(ChooseMessage, dict(message_chosen=1), timeout_happened=True)
        # elif self.player.id_in_group == 3:
        #     yield ChooseMessage, dict(message_chosen=1)
        # elif self.player.id_in_group == 4:
        #     yield ChooseMessage, dict(message_chosen=2)

        # No real players send the message -> No bot send the message either
        # if self.player.id_in_group == 1 or self.player.id_in_group == 2:
        #     self.player.participant.is_dropout = True
        #     yield Submission(ChooseMessage, dict(message_chosen=1), timeout_happened=True)
        # elif self.player.id_in_group == 3:
        #     yield ChooseMessage, dict(message_chosen=2)
        # elif self.player.id_in_group == 4:
        #     yield ChooseMessage, dict(message_chosen=2)


        # If there there are 3 bots and 1 real player, the bots should copy the player's response
        if self.player.id_in_group != 4:
            self.player.participant.is_dropout = True
            yield Submission(ChooseMessage, dict(message_chosen=1), timeout_happened=True)
        else:
            yield ChooseMessage, dict(message_chosen=1)
